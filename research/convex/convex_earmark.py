#!/usr/bin/env python3
"""Read-only historical audit of Ethereum Convex V1 Booster CRV earmark incentives.

Does not sign, send, claim, buy or estimate unclaimed revenue. Only successful
historical transfers to exact transaction submitters are considered paid evidence.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from eth_abi import decode
from eth_utils import keccak

BOOSTER="0xF403C135812408BFbE8713b5A23a04b3D48AAE31"
CRV="0xD533a949740bb3306d119CC777fa900bA034cd52"
PROVIDERS=("https://ethereum-rpc.publicnode.com",
           "https://eth.llamarpc.com","https://eth.drpc.org")
TRANSFER="0x"+keccak(text="Transfer(address,address,uint256)").hex()
EARMARK="0x"+keccak(text="earmarkRewards(uint256)")[:4].hex()
ALLOW={"eth_chainId","eth_blockNumber","eth_getCode","eth_call","eth_getLogs",
       "eth_getTransactionReceipt","eth_getTransactionByHash"}
WINDOW_BLOCKS=7400
CHUNK=250
MAX_LOGS=140
MAX_RECEIPTS=80

def rpc(url,method,params=()):
    if method not in ALLOW:
        raise ValueError("Signing or mutating RPC blocked: "+method)
    payload=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":list(params)}).encode()
    req=urllib.request.Request(url,data=payload,
        headers={"Content-Type":"application/json","User-Agent":"ProtocolConvexReadonly/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=18) as f: data=json.load(f)
    except Exception as e: raise RuntimeError(method+": "+str(e)) from e
    if "result" not in data or "error" in data:
        raise RuntimeError(method+": "+str(data.get("error","missing result")))
    return data["result"]

def sel(text):return "0x"+keccak(text=text)[:4].hex()

def ethcall(url,method):
    raw=rpc(url,"eth_call",[{"to":BOOSTER,"data":sel(method)},"latest"])
    if not isinstance(raw,str) or len(raw)<66:raise RuntimeError("Invalid eth_call result")
    return raw

def inspect(url):
    if int(rpc(url,"eth_chainId"),16)!=1:raise RuntimeError("Expected Ethereum mainnet chain id 1")
    if rpc(url,"eth_getCode",[BOOSTER,"latest"]) in ("0x","0x0","0x00"):
        raise RuntimeError("Official Booster bytecode absent")
    if rpc(url,"eth_getCode",[CRV,"latest"]) in ("0x","0x0","0x00"):
        raise RuntimeError("CRV bytecode absent")
    block=int(rpc(url,"eth_blockNumber"),16)
    start=max(0,block-WINDOW_BLOCKS+1)
    incentive=decode(["uint256"],bytes.fromhex(ethcall(url,"earmarkIncentive()")[2:]))[0]
    is_shutdown=decode(["bool"],bytes.fromhex(ethcall(url,"isShutdown()")[2:]))[0]
    try:pool_length=decode(["uint256"],bytes.fromhex(ethcall(url,"poolLength()")[2:]))[0]
    except Exception as e:pool_length_error=str(e)[:160];pool_length=None
    else:pool_length_error=None
    all_logs=[]
    for lo in range(start,block+1,CHUNK):
        hi=min(block,lo+CHUNK-1)
        logs=rpc(url,"eth_getLogs",[{"address":CRV,
            "fromBlock":hex(lo),"toBlock":hex(hi),
            "topics":[TRANSFER,"0x"+"00"*12+BOOSTER[2:].lower()]}])
        all_logs.extend(x for x in logs if not x.get("removed",False))
        if len(all_logs)>MAX_LOGS:
            raise RuntimeError("Safety cap: too many CRV transfers; narrow scan. Not zero.")
    # Transfers can happen in many transactions; inspect each hash only once.
    grouped={}
    for ev in all_logs:
        grouped.setdefault(ev["transactionHash"].lower(),[]).append(ev)
    records=[];errors=[]
    for i,(txhash,transfers) in enumerate(grouped.items()):
        if i>=MAX_RECEIPTS:
            errors.append({"transaction":txhash,"error":"Receipt cap reached; omitted"})
            continue
        try:
            tx=rpc(url,"eth_getTransactionByHash",[txhash])
            receipt=rpc(url,"eth_getTransactionReceipt",[txhash])
            if not tx or not receipt or int(receipt.get("status","0x0"),16)!=1:
                raise ValueError("Tx/receipt missing or failed")
            inputdata=tx.get("input","0x")
            direct=(tx.get("to") or "").lower()==BOOSTER.lower() and inputdata[:10].lower()==EARMARK.lower()
            submitted_from=tx["from"].lower()
            actual_caller_reward=0
            transfers_out=[]
            for ev in transfers:
                topics=ev.get("topics",[])
                if len(topics)<3 or topics[0].lower()!=TRANSFER:continue
                recipient="0x"+topics[2][-40:]
                amount=int(ev["data"],16)
                reward_to_tx_sender=(recipient.lower()==submitted_from)
                if direct and reward_to_tx_sender:actual_caller_reward+=amount
                transfers_out.append({"to":recipient,"amount_crv_raw":str(amount),
                                      "is_transaction_sender":reward_to_tx_sender})
            gas=int(receipt["gasUsed"],16)*int(receipt["effectiveGasPrice"],16)
            records.append({
                "tx":txhash,"block":int(receipt["blockNumber"],16),
                "tx_from":tx["from"],"tx_to":tx.get("to"),
                "input_selector":inputdata[:10],"direct_earmark_call":direct,
                "direct_reward_to_sender_crv_raw":str(actual_caller_reward),
                "direct_reward_to_sender_crv_units":str(Decimal(actual_caller_reward)/Decimal(10**18)),
                "gas_eth_units":str(Decimal(gas)/Decimal(10**18)),
                "transfers_from_booster":transfers_out[:30],
                "note":"No token liquidation or USD cash value proved. Intermediary contracts excluded from direct submitter PnL."})
        except Exception as e:
            errors.append({"tx":txhash,"error":str(e)[:180]})
    matched=[x for x in records if x["direct_earmark_call"] and Decimal(x["direct_reward_to_sender_crv_units"])>0]
    total_crv=sum((Decimal(x["direct_reward_to_sender_crv_units"]) for x in matched),Decimal(0))
    total_gas=sum((Decimal(x["gas_eth_units"]) for x in matched),Decimal(0))
    keepers={}
    for x in matched:
        keepers[x["tx_from"].lower()]=keepers.get(x["tx_from"].lower(),0)+1
    return {
        "status":"partial" if errors else "bounded_historical_observation_not_live_opportunity",
        "observed_at_utc":datetime.now(timezone.utc).isoformat(),
        "provider":url,"chain_id":1,"from_block":start,"to_block":block,
        "booster":BOOSTER,"token":CRV,"earmark_selector":EARMARK,
        "booster_is_shutdown":is_shutdown,"earmark_incentive_basis_points":incentive,
        "pools":pool_length,"pool_length_error":pool_length_error,
        "candidate_crv_transfer_logs":len(all_logs),"distinct_tx":len(grouped),
        "direct_earmark_calls_paid":len(matched),
        "direct_paid_crv_total_units":str(total_crv),
        "gas_eth_total_for_paid_direct_calls":str(total_gas),
        "successful_direct_keepers":keepers,
        "transfers":records,"errors":errors,
        "scope_warning":"Historical ~7400 Ethereum blocks of only CRV Transfers originating from official Booster. This does not enumerate all pools, indirect contracts or current unswept rewards. No current payable action found.",
        "capital_spent_usd":0,"cash_user_received_usd":0}

def main():
    os.makedirs("reports",exist_ok=True)
    attempts=[];data=None
    for provider in PROVIDERS:
        try:
            data=inspect(provider)
            attempts.append({"provider":provider,"status":data["status"]})
            break
        except Exception as e:
            attempts.append({"provider":provider,"status":"incomplete","error":str(e)[:250]})
    if data is None:data={"status":"incomplete","message":"No usable provider. NOT zero rewards."}
    data["attempts"]=attempts
    with open("reports/convex-historical.json","w") as f:json.dump(data,f,indent=2)
    print(json.dumps({"status":data["status"],
      "booster_is_shutdown":data.get("booster_is_shutdown"),
      "incentive_bps":data.get("earmark_incentive_basis_points"),
      "pool_length":data.get("pools"),
      "candidate_transfer_logs":data.get("candidate_crv_transfer_logs"),
      "direct_paid_call_count":data.get("direct_earmark_calls_paid"),
      "paid_crv":data.get("direct_paid_crv_total_units"),
      "gas_eth":data.get("gas_eth_total_for_paid_direct_calls"),
      "keepers":data.get("successful_direct_keepers"),
      "attempts":attempts},indent=2))
    return 0 if data["status"]!="incomplete" else 2
if __name__=="__main__":sys.exit(main())
