#!/usr/bin/env python3
"""Read-only Convex V2 locker KickReward receipt census; no signing/transactions."""
import json,os,sys
from datetime import datetime,timezone
from decimal import Decimal
from eth_abi import decode
from eth_utils import keccak
import convex_earmark as b

LOCKER="0x72a19342e8F1838460eBFCCEf09F6585e32db86E"
CVX="0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"
KICK="0x"+keccak(text="KickReward(address,address,uint256)").hex()
WINDOW=7400
CHUNK=250
MAX=90
def read_param(url,sig):
    result=b.rpc(url,"eth_call",[{"to":LOCKER,"data":b.sel(sig)},"latest"])
    return decode(["uint256"],bytes.fromhex(result[2:]))[0]
def audit(url):
    if int(b.rpc(url,"eth_chainId"),16)!=1:raise RuntimeError("Wrong chain")
    if b.rpc(url,"eth_getCode",[LOCKER,"latest"]) in ("0x","0x0","0x00"):
        raise RuntimeError("No live V2 locker bytecode")
    params={p:read_param(url,p+"()") for p in
            ("kickRewardPerEpoch","kickRewardEpochDelay","denominator","rewardsDuration")}
    block=int(b.rpc(url,"eth_blockNumber"),16)
    start=max(0,block-WINDOW+1)
    logs=[]
    for lo in range(start,block+1,CHUNK):
        hi=min(block,lo+CHUNK-1)
        logs+=b.rpc(url,"eth_getLogs",[{"address":LOCKER,"topics":[KICK],
                     "fromBlock":hex(lo),"toBlock":hex(hi)}])
        if len(logs)>MAX:raise RuntimeError("Exceeded 90 KickReward events; narrow sample")
    records=[];errs=[]
    for i,log in enumerate(logs):
        try:
            if len(log["topics"])!=3 or log["topics"][0].lower()!=KICK:
                raise ValueError("Event signature mismatch")
            kicker="0x"+log["topics"][1][-40:]
            kicked="0x"+log["topics"][2][-40:]
            amount=decode(["uint256"],bytes.fromhex(log["data"][2:]))[0]
            row={"transaction":log["transactionHash"],"kicker":kicker,
                 "kicked":kicked,"reward_cvx_units":str(Decimal(amount)/Decimal(10**18)),
                 "block":int(log["blockNumber"],16)}
            if i<MAX:
                tx=b.rpc(url,"eth_getTransactionByHash",[log["transactionHash"]])
                receipt=b.rpc(url,"eth_getTransactionReceipt",[log["transactionHash"]])
                if not tx or not receipt or int(receipt["status"],16)!=1:raise ValueError("Missing successful tx")
                fees=Decimal(int(receipt["gasUsed"],16)*int(receipt["effectiveGasPrice"],16))/Decimal(10**18)
                row.update({"tx_sender":tx["from"],"sender_is_kicker":tx["from"].lower()==kicker.lower(),
                           "gas_eth_units":str(fees)})
            records.append(row)
        except Exception as exc:
            errs.append({"transaction":log.get("transactionHash"),"error":str(exc)[:220]})
    total=sum((Decimal(x["reward_cvx_units"]) for x in records),Decimal(0))
    unique={}
    for x in records:
        unique[x["kicker"].lower()]=unique.get(x["kicker"].lower(),0)+1
    return {"status":"partial" if errs else "bounded_historical_observation",
        "chain_id":1,"locker":LOCKER,"cvx_token":CVX,"observed_at":datetime.now(timezone.utc).isoformat(),
        "window_from_block":start,"window_to_block":block,
        "current_parameters":params,"kick_events":len(logs),"receipt_checked":len(records),
        "total_historical_kick_cvx":str(total),"keeper_concentration":unique,
        "events":records,"errors":errs,
        "scope":"Historical ~7400 blocks; an event records past received CVX, not a currently eligible user. No claims/actions are taken.",
        "cash_earned_by_user":0,"capital_spent_usd":0}
def main():
    os.makedirs("reports",exist_ok=True)
    attempts=[];record=None
    for provider in b.PROVIDERS:
        try:record=audit(provider);attempts.append({"provider":provider,"status":record["status"]});break
        except Exception as exc:attempts.append({"provider":provider,"status":"incomplete","error":str(exc)[:240]})
    if record is None:record={"status":"incomplete","note":"No usable provider. NOT zero bounties"}
    record["attempts"]=attempts
    with open("reports/convex-kicks.json","w") as f:json.dump(record,f,indent=2)
    print(json.dumps({k:record.get(k) for k in
        ("status","current_parameters","kick_events","total_historical_kick_cvx","keeper_concentration","attempts")},indent=2))
    return 0 if record["status"]!="incomplete" else 2
if __name__=="__main__":sys.exit(main())
