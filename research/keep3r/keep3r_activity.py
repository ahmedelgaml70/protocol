#!/usr/bin/env python3
"""Read-only Keep3r V2 historical payment evidence in bounded recent Ethereum blocks."""
import json, os, sys
from collections import defaultdict
from decimal import Decimal
from datetime import datetime,timezone
from eth_abi import decode
from eth_utils import keccak
import keep3r_funding as k

TOPIC="0x"+keccak(text="KeeperWork(address,address,address,uint256,uint256)").hex()
WINDOW=7200
CHUNK=300
MAX_EVENTS=200
MAX_RECEIPTS=24

def activity(url):
    if int(k.rpc(url,"eth_chainId"),16)!=1:raise RuntimeError("Wrong chain")
    tip=int(k.rpc(url,"eth_blockNumber"),16)
    start=max(0,tip-WINDOW+1)
    logs=[]
    for block in range(start,tip+1,CHUNK):
        end=min(tip,block+CHUNK-1)
        part=k.rpc(url,"eth_getLogs",[{"address":k.REGISTRY,
            "fromBlock":hex(block),"toBlock":hex(end),"topics":[TOPIC]}])
        logs.extend([x for x in part if not x.get("removed",False)])
        if len(logs)>MAX_EVENTS:raise RuntimeError("Event cap exceeded; data incomplete")
    items=[]; problems=[]
    for i,x in enumerate(logs):
        try:
            topics=x["topics"]
            if len(topics)!=4 or topics[0].lower()!=TOPIC:
                raise ValueError("Wrong event topics")
            payment,gasleft=decode(["uint256","uint256"],bytes.fromhex(x["data"][2:]))
            credit="0x"+topics[1][-40:]
            job="0x"+topics[2][-40:]
            keeper="0x"+topics[3][-40:]
            obj={"tx":x["transactionHash"],"block":int(x["blockNumber"],16),
                 "credit_token":credit,"job":job,"keeper":keeper,
                 "payment_raw":str(payment),"event_gas_left":gasleft,
                 "receipt_status":"not_inspected"}
            if i<MAX_RECEIPTS:
                try:
                    rec=k.rpc(url,"eth_getTransactionReceipt",[obj["tx"]])
                    tx=k.rpc(url,"eth_getTransactionByHash",[obj["tx"]])
                    if not rec or not tx or int(rec.get("status","0x0"),16)!=1:
                        raise ValueError("Receipt missing or not successful")
                    fee=int(rec["gasUsed"],16)*int(rec["effectiveGasPrice"],16)
                    obj["receipt_status"]="success"
                    obj["sender"]=tx["from"]
                    obj["gas_cost_eth_units"]=str(Decimal(fee)/Decimal(10**18))
                    obj["sender_is_keeper"]=tx["from"].lower()==keeper.lower()
                except Exception as exc:
                    obj["receipt_status"]="incomplete"
                    obj["receipt_error"]=str(exc)[:220]
            items.append(obj)
        except Exception as exc:
            problems.append({"tx":x.get("transactionHash"),"error":str(exc)[:200]})
    groups=defaultdict(list)
    for item in items:groups[item["job"].lower()].append(item)
    return {"status":"sampled_historical_payments_not_current_availability",
            "provider":url,"utc":datetime.now(timezone.utc).isoformat(),
            "start_block":start,"end_block":tip,
            "matched_KeeperWork_events":len(logs),
            "decoded_events":len(items),"receipt_attempted":min(len(items),MAX_RECEIPTS),
            "jobs":[{"job":j,"count":len(recs),"receipts":recs[:12]} for j,recs in groups.items()],
            "error_count":len(problems),"errors":problems,
            "scope_warning":"History proves past payouts only. Registry credits belong to job contracts. No new keeper eligibility, currently callable jobs, near-term pay, token cashability or net profitability has been established.",
            "capital_spent_usd":0,"income_earned_usd":0}

def main():
    os.makedirs("keep3r_reports",exist_ok=True)
    attempts=[]; result=None
    for url in k.PROVIDERS:
        try:
            result=activity(url)
            attempts.append({"provider":url,"status":"completed"})
            break
        except Exception as exc:
            attempts.append({"provider":url,"status":"incomplete","error":str(exc)[:220]})
    if result is None:
        result={"status":"incomplete","note":"Public RPC failed: not evidence of zero events"}
    result["attempts"]=attempts
    with open("keep3r_reports/activity.json","w") as f:json.dump(result,f,indent=2)
    print(json.dumps({"status":result["status"],"total_keeperwork_events":result.get("matched_KeeperWork_events"),
                      "jobs":[{"job":r["job"],"count":r["count"]} for r in result.get("jobs",[])],
                      "attempts":attempts},indent=2))
    return 0 if result["status"]!="incomplete" else 2

if __name__=="__main__":sys.exit(main())
