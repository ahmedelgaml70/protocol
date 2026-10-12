#!/usr/bin/env python3
"""Read-only bounded historical 0xSplits PushSplit research; no wallet or signing."""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal
from eth_abi import decode, encode
from eth_utils import keccak
import splits_observer as base

SPLIT = base.SPLIT
FACTORIES = {
    "v2": "0xaDC87646f736d6A82e9a6539cddC488b2aA07f38",
    "v2o1": "0xDc6259E13ec0621e6F19026b2e49D846525548Ed",
    "v2o2": "0x8E8eB0cC6AE34A38B67D5Cf91ACa38f60bc3Ecf4",
}
CHAINS = {
    "base": (8453, "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
             "0x4200000000000000000000000000000000000006",
             ["https://base-rpc.publicnode.com", "https://base.drpc.org", "https://mainnet.base.org"]),
    "optimism": (10, "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
                 "0x4200000000000000000000000000000000000006",
                 ["https://optimism-rpc.publicnode.com", "https://optimism.drpc.org", "https://mainnet.optimism.io"]),
    "arbitrum": (42161, "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
                 "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
                 ["https://arbitrum-one-rpc.publicnode.com", "https://arbitrum.drpc.org", "https://arb1.arbitrum.io/rpc"]),
}
AGES_DAYS = (0, 7, 30, 90)
WINDOW = 1600  # blocks per discrete sample, not continuous history
CREATED = [base.topic("SplitCreated(address,"+SPLIT+",address,address)"),
           base.topic("SplitCreated(address,"+SPLIT+",address,address,bytes32)"),
           base.topic("SplitCreated(address,"+SPLIT+",address,address,uint256)")]
UPDATED = base.topic("SplitUpdated("+SPLIT+")")

def get_block(url, number):
    item = base.rpc(url, "eth_getBlockByNumber", [hex(number), False])
    if not item or item.get("timestamp") is None:
        raise RuntimeError("Historical block unavailable (possibly pruned)")
    return int(item["timestamp"], 16)

def timestamp_block(url, tip, target):
    # Search recent history backwards first; don't demand genesis from pruned RPCs.
    step = min(tip, 200000)
    low = max(0, tip - step)
    while low > 0 and get_block(url, low) > target:
        step = min(tip, step * 2)
        low = max(0, tip - step)
    if get_block(url, low) > target:
        raise RuntimeError("Historical target predates provider history")
    high = tip
    while low < high:
        mid = (low + high + 1) // 2
        if get_block(url, mid) <= target:
            low = mid
        else:
            high = mid - 1
    return low

def windows(url, tip):
    timestamp = get_block(url, tip)
    result = []
    for days in AGES_DAYS:
        try:
            end = tip if not days else timestamp_block(url, tip, timestamp-days*86400)
            start = max(0, end-WINDOW+1)
            result.append({"anchor_days_ago": days, "from_block": start,
                           "to_block": end, "from_timestamp": get_block(url,start),
                           "to_timestamp": get_block(url,end), "status":"sampled"})
        except Exception as exc:
            result.append({"anchor_days_ago": days, "status":"incomplete",
                           "error":str(exc)[:220]})
    return result

def parse_created(log):
    if len(log.get("topics", [])) < 2 or log["topics"][0].lower() not in CREATED:
        raise ValueError("Invalid SplitCreated event topics")
    address = "0x" + log["topics"][1][-40:]
    params = decode([SPLIT], bytes.fromhex(log["data"][2:]))[0]
    if not params[0] or len(params[0]) != len(params[1]) or sum(params[1]) != params[2] or not params[2]:
        raise ValueError("Invalid split allocation tuple")
    return address, params

def verified_config(url, address, initial, tip):
    live = base.call(url,address,"splitHash()")
    if live == keccak(encode([SPLIT],[initial])):
        return initial, "factory_creation_matches_current_hash"
    begin = max(0,tip-6000)
    updates = base.events(url,address,begin,tip,[[UPDATED]],200)
    if not updates:
        raise ValueError("Changed configuration; updated event outside checked history")
    latest = decode([SPLIT],bytes.fromhex(updates[-1]["data"][2:]))[0]
    if live != keccak(encode([SPLIT],[latest])):
        raise ValueError("Most recent visible update does not match current hash")
    return latest, "bounded_latest_update_matches_current_hash"

def inspect_tokens(url, addr, params, cfg, gas_price):
    native = decode(["address"], base.call(url,addr,"NATIVE_TOKEN()"))[0]
    assets = [("USDC",cfg[1],6),("WETH",cfg[2],18),("NATIVE",native,18)]
    observed = []
    for symbol,token,decimals in assets:
        try:
            if symbol!="NATIVE":
                actual=decode(["uint8"],base.call(url,token,"decimals()"))[0]
                if actual!=decimals:
                    raise ValueError("Unexpected "+symbol+" decimals")
            balances = decode(["uint256","uint256"],
                base.call(url,addr,"getSplitBalance(address)",encode(["address"],[token])))
            raw = sum(balances)*params[3]//1000000
            if raw==0:
                continue
            data = base.selector("distribute("+SPLIT+",address,address)") + encode(
                [SPLIT,"address","address"],[params,token,base.FROM]).hex()
            args = {"from":base.FROM,"to":addr,"data":data}
            item = {"symbol":symbol,"token":token,"wallet_balance_raw":str(balances[0]),
                    "warehouse_balance_raw":str(balances[1]),
                    "gross_reward_raw":str(raw),
                    "gross_reward_token_units":str(Decimal(raw)/Decimal(10**decimals)),
                    "simulation":"unverified"}
            try:
                base.rpc(url,"eth_call",[args,"latest"])
                item["simulation"]="eth_call_success_only"
                try:
                    gas=int(base.rpc(url,"eth_estimateGas",[args]),16)
                    item["estimated_gas_units"]=gas
                    item["estimated_native_gas_cost"]=str(Decimal(gas*gas_price)/Decimal(10**18))
                except Exception as exc:
                    item["estimate_error"]=str(exc)[:180]
            except Exception as exc:
                item["simulation"]="eth_call_failed:"+str(exc)[:180]
            observed.append(item)
        except Exception as exc:
            observed.append({"symbol":symbol,"status":"incomplete","error":str(exc)[:180]})
    return observed

def scan(url, name):
    cfg=CHAINS[name]
    actual=int(base.rpc(url,"eth_chainId"),16)
    if actual!=cfg[0]:
        raise RuntimeError("Chain ID mismatch: "+str(actual))
    tip=int(base.rpc(url,"eth_blockNumber"),16)
    periods=windows(url,tip)
    price=int(base.rpc(url,"eth_gasPrice"),16)
    enabled={}
    for version,address in FACTORIES.items():
        code=base.rpc(url,"eth_getCode",[address,"latest"])
        enabled[version]=code not in ("0x","0x0","0x00")
    if not any(enabled.values()):
        raise RuntimeError("No factory bytecode found")
    samples=[]; rejected=[]; candidates=[]; seen=set(); total=0
    completed=0; incomplete=0
    for version,address in FACTORIES.items():
        if not enabled[version]:
            samples.append({"version":version,"status":"no_code"})
            continue
        for period in periods:
            if period.get("status")=="incomplete":
                incomplete+=1
                samples.append({"version":version,"anchor_days_ago":period["anchor_days_ago"],
                                "status":"incomplete","error":period["error"]})
                continue
            try:
                logs=base.events(url,address,period["from_block"],period["to_block"],[CREATED],200)
                completed+=1
            except Exception as exc:
                incomplete+=1
                samples.append({"version":version,"anchor_days_ago":period["anchor_days_ago"],
                                "status":"incomplete","error":str(exc)[:220]})
                continue
            total+=len(logs)
            if total>120:
                raise RuntimeError("Event safety cap hit; narrow sample")
            samples.append({"version":version,"anchor_days_ago":period["anchor_days_ago"],
                            "from_block":period["from_block"],"to_block":period["to_block"],
                            "creation_events":len(logs)})
            for log in logs:
                try:
                    split,initial=parse_created(log)
                    if split.lower() in seen:
                        continue
                    seen.add(split.lower())
                    if base.rpc(url,"eth_getCode",[split,"latest"]) in ("0x","0x0","0x00"):
                        raise ValueError("Split has no code")
                    current,prov=verified_config(url,split,initial,tip)
                    if not 0 < current[3] <= 65000:
                        if current[3]==0:
                            continue
                        raise ValueError("Incentive out of documented range")
                    tokens=inspect_tokens(url,split,current,cfg,price)
                    if not any(t.get("gross_reward_raw") for t in tokens):
                        continue
                    candidates.append({"split":split,"factory_version":version,
                                       "created_at_block":int(log["blockNumber"],16),
                                       "incentive_parts_per_million":current[3],
                                       "configuration_provenance":prov,"tokens":tokens,
                                       "status":"RESEARCH_ONLY_UNVERIFIED"})
                except Exception as exc:
                    rejected.append({"version":version,"tx":log.get("transactionHash"),
                                     "error":str(exc)[:220]})
    if completed==0:
        raise RuntimeError("All factory time-window scans incomplete; no zero-opportunity inference")
    status="partial_observation_not_profit" if incomplete else "sampled_observation_not_profit"
    return {"status":status,"chain":name,"chain_id":cfg[0],
            "completed_factory_windows":completed,"incomplete_factory_windows":incomplete,
            "provider":url,"observed_at_utc":datetime.now(timezone.utc).isoformat(),
            "sampled_windows":periods,"factory_bytecode_present":enabled,
            "factory_window_counts":samples,"sampled_creation_events":total,
            "unique_contracts_considered":len(seen),"positive_reward_screens":len(candidates),
            "candidates":candidates,"rejected":rejected,
            "scope_warning":"Four short non-contiguous factory creation samples, three Push Split versions, USDC/WETH/native only. NOT all older contracts, all versions, all tokens or current executable profit. No realized receipts verified.",
            "money_spent_usd":0,"income_realized_usd":0}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--chain",choices=CHAINS,required=True)
    opt=parser.parse_args()
    os.makedirs("expanded_reports",exist_ok=True)
    attempts=[]; result=None
    for provider in CHAINS[opt.chain][3]:
        try:
            result=scan(provider,opt.chain)
            attempts.append({"provider":provider,"status":result["status"]})
            break
        except Exception as exc:
            attempts.append({"provider":provider,"status":"incomplete","error":str(exc)[:280]})
    if result is None:
        result={"status":"incomplete","chain":opt.chain,
                "message":"All RPC providers failed, no zero-opportunity inference."}
    result["attempts"]=attempts
    with open("expanded_reports/"+opt.chain+".json","w") as f:
        json.dump(result,f,indent=2)
    print(json.dumps({"chain":opt.chain,"status":result["status"],
                      "events":result.get("sampled_creation_events"),
                      "reward_screens":result.get("positive_reward_screens"),
                      "attempts":attempts},indent=2))
    return 0 if result["status"] in ("sampled_observation_not_profit","partial_observation_not_profit") else 2

if __name__=="__main__":
    sys.exit(main())
