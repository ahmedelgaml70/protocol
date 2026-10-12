#!/usr/bin/env python3
"""Read-only preflight for recent Keep3r Yearn-like job strategy workability."""
import json,os,sys
from datetime import datetime,timezone
from eth_abi import decode,encode
from eth_utils import keccak
import keep3r_funding as base

JOB="0xf4f748d45e03a70a9473394b28c3c7b5572dfa82"
WORKED_TOPIC="0x"+keccak(text="KeeperWorked(address)").hex()
BLOCK_WINDOW=7200
LOG_CHUNK=300
MAX_STRATEGIES=20
DUMMY="0x1111111111111111111111111111111111111111"

def strategy_from_log(row):
    if row["address"].lower()!=JOB or not row.get("topics") or row["topics"][0].lower()!=WORKED_TOPIC:
        raise ValueError("Wrong job or event")
    if len(row["topics"])!=1 or len(bytes.fromhex(row["data"][2:]))!=32:
        raise ValueError("Unexpected KeeperWorked ABI")
    return decode(["address"],bytes.fromhex(row["data"][2:]))[0]

def view_job(url,signature,addr=None):
    payload=base.selector(signature)
    if addr is not None:payload+=encode(["address"],[addr]).hex()
    return base.rpc(url,"eth_call",[{"from":DUMMY,"to":JOB,"data":payload},"latest"])

def scan(url):
    if int(base.rpc(url,"eth_chainId"),16)!=1:raise RuntimeError("Not Ethereum mainnet")
    if base.rpc(url,"eth_getCode",[JOB,"latest"]) in ("0x","0x0","0x00"):
        raise RuntimeError("Active job has no code")
    tip=int(base.rpc(url,"eth_blockNumber"),16)
    begin=max(0,tip-BLOCK_WINDOW+1)
    logs=[]
    for start in range(begin,tip+1,LOG_CHUNK):
        end=min(start+LOG_CHUNK-1,tip)
        logs+=base.rpc(url,"eth_getLogs",[{"address":JOB,"topics":[WORKED_TOPIC],
                    "fromBlock":hex(start),"toBlock":hex(end)}])
    seen=[];skipped=0
    for ev in logs:
        try:
            strat=strategy_from_log(ev)
            if strat.lower() not in [x.lower() for x in seen]:seen.append(strat)
        except Exception:skipped+=1
    rows=[]
    for addr in seen[:MAX_STRATEGIES]:
        item={"strategy":addr,"workable":"unknown","dummy_work":"not_run"}
        try:
            raw=view_job(url,"workable(address)",addr)
            item["workable"]=bool(decode(["bool"],bytes.fromhex(raw[2:]))[0])
        except Exception as exc:
            item["workable"]="unavailable_or_reverted"
            item["workable_error"]=str(exc)[:170]
        if item["workable"] is True:
            try:
                # Simulation only; no sign, send, or state changes.
                view_job(url,"work(address)",addr)
                item["dummy_work"]="simulated_success_only"
            except Exception as exc:
                item["dummy_work"]="reverted_for_unregistered_dummy"
                item["dummy_error"]=str(exc)[:190]
        rows.append(item)
    return {"status":"read_only_historical_strategy_preflight",
            "utc":datetime.now(timezone.utc).isoformat(),"chain":1,"provider":url,
            "job":JOB,"from_block":begin,"to_block":tip,
            "keeperworked_logs":len(logs),"decoding_errors":skipped,
            "unique_strategies":len(seen),"checked":len(rows),
            "currently_workable_true":sum(x["workable"] is True for x in rows),
            "unregistered_dummy_simulated_success":sum(x["dummy_work"]=="simulated_success_only" for x in rows),
            "strategies":rows,"unseen_strategies":max(0,len(seen)-len(rows)),
            "limitation":"Current workable status is not a future payout. A true value is NOT executable by a fresh keeper without eligibility, a timely transaction and profitable gas. Never broadcast.",
            "money_spent_usd":0,"user_earned_usd":0}

def main():
    os.makedirs("keep3r_reports",exist_ok=True)
    attempts=[];result=None
    for provider in base.PROVIDERS:
        try:
            result=scan(provider)
            attempts.append({"provider":provider,"status":result["status"]})
            break
        except Exception as exc:
            attempts.append({"provider":provider,"status":"incomplete","error":str(exc)[:240]})
    if result is None:result={"status":"incomplete","note":"Data access failed; not zero"}
    result["attempts"]=attempts
    with open("keep3r_reports/preflight.json","w") as f:json.dump(result,f,indent=2)
    print(json.dumps({"status":result["status"],"keeperworked_logs":result.get("keeperworked_logs"),
                       "unique_strategies":result.get("unique_strategies"),
                       "currently_workable_true":result.get("currently_workable_true"),
                       "unregistered_dummy_simulated_success":result.get("unregistered_dummy_simulated_success"),
                       "strategies":result.get("strategies",[])[:20],"attempts":attempts},indent=2))
    return 0 if result["status"]!="incomplete" else 2
if __name__=="__main__":sys.exit(main())
