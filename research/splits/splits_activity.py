#!/usr/bin/env python3
"""Read-only sampled historical distributions from previously deployed PushSplits.

Records verified emitter factory and ERC20 beneficiary transfer receipts only.
Not a live bounty finder and never sends transactions.
"""
import argparse
import json
import os
import sys
from datetime import datetime,timezone
from decimal import Decimal

from eth_abi import decode
import splits_observer as rpcbase
import splits_expanded as expanded

DISTRIBUTED=rpcbase.topic("SplitDistributed(address,address,uint256)")
TRANSFER=rpcbase.topic("Transfer(address,address,uint256)")
FACTORY_ADDRS={a.lower():v for v,a in expanded.FACTORIES.items()}
MAX_ACTIVITY_EVENTS=200
MAX_RECEIPTS=14

def fetch_logs(url, start, end):
    records=[]
    for first in range(start,end+1,200):
        last=min(first+199,end)
        part=rpcbase.rpc(url,"eth_getLogs",[{
            "fromBlock":hex(first),"toBlock":hex(last),
            "topics":[DISTRIBUTED]}])
        records.extend(x for x in part if not x.get("removed",False))
        if len(records)>MAX_ACTIVITY_EVENTS:
            raise RuntimeError("Too many events; lower scan window (not zero observations)")
    return records

def decode_event(log):
    topics=log.get("topics",[])
    if len(topics)!=3 or topics[0].lower()!=DISTRIBUTED:
        raise ValueError("Not a SplitDistributed event")
    return {"emitter":log["address"],"token":"0x"+topics[1][-40:],
            "distributor":"0x"+topics[2][-40:],
            "distributed_amount_raw":str(int(log["data"],16)),
            "tx":log["transactionHash"],"block":int(log["blockNumber"],16)}

def verify_emitter(url, emitter):
    factory=decode(["address"],rpcbase.call(url,emitter,"FACTORY()"))[0]
    version=FACTORY_ADDRS.get(factory.lower())
    if not version:
        raise ValueError("Not a known three-generation PushSplit factory")
    return version

def receipt_proof(url, row):
    receipt=rpcbase.rpc(url,"eth_getTransactionReceipt",[row["tx"]])
    tx=rpcbase.rpc(url,"eth_getTransactionByHash",[row["tx"]])
    if not receipt or not tx or int(receipt.get("status","0x0"),16)!=1:
        raise ValueError("Missing or failed transaction")
    sender=tx["from"]
    total=0
    for entry in receipt.get("logs",[]):
        top=entry.get("topics",[])
        if (entry["address"].lower()!=row["token"].lower() or len(top)<3
                or top[0].lower()!=TRANSFER):
            continue
        transfer_from="0x"+top[1][-40:]
        transfer_to="0x"+top[2][-40:]
        if (transfer_from.lower()==row["emitter"].lower()
                and transfer_to.lower()==row["distributor"].lower()):
            total+=int(entry["data"],16)
    gas=int(receipt.get("gasUsed","0x0"),16)
    price=int(receipt.get("effectiveGasPrice","0x0"),16)
    layer1=int(receipt.get("l1Fee","0x0"),16) if receipt.get("l1Fee") else 0
    return {"transaction_from":sender,
            "is_distributor_transaction_sender":sender.lower()==row["distributor"].lower(),
            "erc20_direct_transfer_from_split_to_distributor_raw":str(total),
            "reported_native_gas_fee_units":str(Decimal(gas*price+layer1)/Decimal(10**18)),
            "gas_l1fee_field_present":bool(receipt.get("l1Fee")),
            "note":"Transfer can be other beneficiary payment; not independently proved caller incentive or net profit."}

def scan(url,name):
    chain=expanded.CHAINS[name]
    if int(rpcbase.rpc(url,"eth_chainId"),16)!=chain[0]:
        raise RuntimeError("Wrong chain")
    tip=int(rpcbase.rpc(url,"eth_blockNumber"),16)
    periods=expanded.windows(url,tip)
    observed=[]; rejected=[]; samples=[]; seen=set(); completed=0; incomplete=0
    for period in periods:
        if period.get("status")=="incomplete":
            incomplete+=1
            samples.append({"anchor_days_ago":period["anchor_days_ago"],
                            "status":"incomplete","error":period["error"]})
            continue
        try:
            logs=fetch_logs(url,period["from_block"],period["to_block"])
        except Exception as exc:
            incomplete+=1
            samples.append({"anchor_days_ago":period["anchor_days_ago"],
                            "status":"incomplete","error":str(exc)[:250]})
            continue
        completed+=1
        samples.append({"anchor_days_ago":period["anchor_days_ago"],
                        "status":"sampled","count_all_topic_matches":len(logs)})
        for log in logs:
            try:
                item=decode_event(log)
                if item["tx"].lower() in seen:
                    continue
                version=verify_emitter(url,item["emitter"])
                seen.add(item["tx"].lower())
                item["factory_version"]=version
                if len(observed)<MAX_RECEIPTS:
                    try:
                        item["receipt"]=receipt_proof(url,item)
                    except Exception as exc:
                        item["receipt"]={"status":"incomplete","error":str(exc)[:200]}
                else:
                    item["receipt"]={"status":"uninspected_beyond_receipt_cap"}
                observed.append(item)
            except Exception as exc:
                rejected.append({"tx":log.get("transactionHash"),"error":str(exc)[:200]})
    if completed==0:
        raise RuntimeError("No historical distribution log window completed")
    return {"status":"partial_observation_not_profit" if incomplete else "sampled_observation_not_profit",
            "chain":name,"provider":url,"utc":datetime.now(timezone.utc).isoformat(),
            "time_windows":samples,"matching_verified_push_split_transactions":len(observed),
            "receipt_checked":min(len(observed),MAX_RECEIPTS),
            "transactions":observed,"rejected":rejected,
            "scope":"Historical SplitDistributed emissions from three factory generations in noncontiguous 1600-block windows. Neither future payouts nor presently funded balances are established.",
            "money_spent_usd":0,"realized_income_usd":0}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--chain",choices=expanded.CHAINS,required=True)
    name=ap.parse_args().chain
    os.makedirs("activity_reports",exist_ok=True)
    attempts=[]; result=None
    for url in expanded.CHAINS[name][3]:
        try:
            result=scan(url,name)
            attempts.append({"provider":url,"status":result["status"]})
            break
        except Exception as exc:
            attempts.append({"provider":url,"status":"incomplete","error":str(exc)[:200]})
    if result is None:
        result={"status":"incomplete","chain":name,"message":"No full or partial successful window; not zero activity."}
    result["attempts"]=attempts
    with open("activity_reports/"+name+".json","w") as f:
        json.dump(result,f,indent=2)
    print(json.dumps({"chain":name,"status":result["status"],
                      "historical_verified_tx":result.get("matching_verified_push_split_transactions"),
                      "attempts":attempts},indent=2))
    return 0 if result["status"]!="incomplete" else 2

if __name__=="__main__":
    sys.exit(main())
