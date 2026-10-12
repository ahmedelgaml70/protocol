#!/usr/bin/env python3
"""Read-only 0xSplits V2o2 PushSplit screen. No wallet, signing or transactions."""
import json, os, sys, time, urllib.request
from decimal import Decimal
from datetime import datetime, timezone
from eth_abi import decode, encode
from eth_utils import keccak

FACTORY = "0x8E8eB0cC6AE34A38B67D5Cf91ACa38f60bc3Ecf4"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
SPLIT = "(address[],uint256[],uint256,uint16)"
SOURCES = (("drpc", "https://base.drpc.org"),
           ("base", "https://mainnet.base.org"),
           ("publicnode", "https://base-rpc.publicnode.com"),
           ("llamarpc", "https://base.llamarpc.com"),
           ("blastapi", "https://base-mainnet.public.blastapi.io"))
FROM = "0x1111111111111111111111111111111111111111"
ALLOWED = {"eth_chainId", "eth_blockNumber", "eth_getCode", "eth_getLogs",
           "eth_call", "eth_estimateGas", "eth_gasPrice"}

def selector(signature):
    return "0x" + keccak(text=signature)[:4].hex()

def topic(signature):
    return "0x" + keccak(text=signature).hex()

def rpc(url, method, params=()):
    if method not in ALLOWED:
        raise ValueError("Transaction/unsupported RPC blocked: " + method)
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":list(params)}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json","Accept":"application/json",
        "User-Agent":"ProtocolReadOnlyObserver/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=16) as res:
            obj = json.load(res)
    except Exception as exc:
        raise RuntimeError(method + ": " + str(exc)) from exc
    if "error" in obj or "result" not in obj:
        raise RuntimeError(str(obj.get("error", "missing result")))
    return obj["result"]

def events(url, address, start, end, topics, chunk=200):
    result = []
    for b in range(start, end+1, chunk):
        r = min(end, b+chunk-1)
        result.extend(rpc(url,"eth_getLogs",[{
            "address":address,"fromBlock":hex(b),"toBlock":hex(r),"topics":topics}]))
    return [e for e in result if not e.get("removed",False)]

def call(url, address, sig, args=b""):
    return bytes.fromhex(rpc(url,"eth_call",[
        {"to":address,"data":selector(sig)+args.hex()},"latest"])[2:])

def assert_chain_and_code(url):
    chain = int(rpc(url,"eth_chainId"),16)
    if chain != 8453:
        raise RuntimeError("Wrong chain: "+str(chain))
    code = rpc(url,"eth_getCode",[FACTORY,"latest"])
    if code in ("0x","0x0","0x00"):
        raise RuntimeError("No bytecode at expected V2o2 factory")
    return int(rpc(url,"eth_blockNumber"),16)

def scan(url, max_blocks=4000):
    tip = assert_chain_and_code(url)
    begin = max(0,tip-max_blocks+1)
    variants = [topic("SplitCreated(address,"+SPLIT+",address,address,bytes32)"),
                topic("SplitCreated(address,"+SPLIT+",address,address,uint256)")]
    creation = events(url,FACTORY,begin,tip,[variants])
    if len(creation)>100:
        raise RuntimeError("Too many created events; narrow interval")
    update_topic = topic("SplitUpdated("+SPLIT+")")
    found, rejected = [], []
    dec = decode(["uint8"],call(url,USDC,"decimals()"))[0]
    if dec>36: raise RuntimeError("Unreasonable USDC decimals")
    for ev in creation:
        try:
            addr = "0x"+ev["topics"][1][-40:]
            if rpc(url,"eth_getCode",[addr,"latest"]) in ("0x","0x0","0x00"):
                raise ValueError("Split not deployed")
            created = int(ev["blockNumber"],16)
            updates = events(url,addr,created,tip,[[update_topic]])
            if not updates:
                raise ValueError("No SplitUpdated event")
            current = decode([SPLIT], bytes.fromhex(updates[-1]["data"][2:]))[0]
            onchain_hash = call(url,addr,"splitHash()")
            if onchain_hash != keccak(encode([SPLIT],[current])):
                raise ValueError("Current split hash differs from logged configuration")
            incentive = current[3]
            if incentive==0: continue
            b = decode(["uint256","uint256"],
                 call(url,addr,"getSplitBalance(address)",encode(["address"],[USDC])))
            bal = b[0]+b[1]
            raw = bal*incentive//1000000
            if raw==0: continue
            item = {"split":addr,"created_block":created,"incentive_units_per_million":incentive,
                    "token":USDC,"wallet_balance_raw":b[0],"warehouse_balance_raw":b[1],
                    "estimated_reward_USDC_units":str(Decimal(raw)/(Decimal(10)**dec)),
                    "simulation":"not_run","status":"UNVERIFIED_READ_ONLY"}
            data = selector("distribute("+SPLIT+",address,address)")+encode(
                [SPLIT,"address","address"],[current,USDC,FROM]).hex()
            callargs = {"from":FROM,"to":addr,"data":data}
            try:
                rpc(url,"eth_call",[callargs,"latest"])
                item["simulation"] = "eth_call success (not executable proof)"
                try:
                    gas = int(rpc(url,"eth_estimateGas",[callargs]),16)
                    price = int(rpc(url,"eth_gasPrice"),16)
                    item["estimated_gas"]=gas
                    item["estimated_native_gas_cost"]=str(Decimal(gas*price)/Decimal(10**18))
                except Exception as exc:
                    item["gas_estimation_error"]=str(exc)[:350]
            except Exception as exc:
                item["simulation"]="failed: "+str(exc)[:350]
            found.append(item)
        except Exception as exc:
            rejected.append({"tx":ev.get("transactionHash"),"reason":str(exc)[:450]})
    return {"status":"observation_not_profit","chain_id":8453,"factory":FACTORY,
            "token":USDC,"start_block":begin,"end_block":tip,
            "scope":"V2o2 PushSplits created in latest 4000 blocks, Base USDC only",
            "creation_events":len(creation),"positive_reward_screens":len(found),
            "candidates":found,"rejected":rejected,
            "warning":"No direct net payout, liquidity, competition or actionability is established."}

def main():
    os.makedirs("splits_reports",exist_ok=True)
    attempts = []
    for name, url in SOURCES:
        started=time.monotonic()
        try:
            result = scan(url)
            result["provider"]=name
            result["timestamp_utc"]=datetime.now(timezone.utc).isoformat()
            status="observation_not_profit"
        except Exception as exc:
            result={"status":"incomplete","error":str(exc)[:700],"provider":name}
            status="incomplete"
        with open("splits_reports/"+name+".json","w") as f:
            json.dump(result,f,indent=2)
        attempts.append({"provider":name,"status":status,"seconds":round(time.monotonic()-started,1)})
        print(name,status,flush=True)
        if status!="incomplete": break
    okay=attempts[-1]["status"]=="observation_not_profit"
    with open("splits_reports/manifest.json","w") as f:
        json.dump({"status":"observation_not_profit" if okay else "incomplete",
                   "attempts":attempts, "money_spent_USD":0},f,indent=2)
    if not okay:
        print("All RPC providers incomplete; NOT a zero-opportunity finding",file=sys.stderr)
    return 0 if okay else 2

if __name__=="__main__":
    sys.exit(main())
