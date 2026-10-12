#!/usr/bin/env python3
"""Read-only current and settled bounty census; never connects a wallet or submits work."""
import json,os,sys,urllib.request
from decimal import Decimal,InvalidOperation
from datetime import datetime,timezone

NETWORKS={
 "arc":{"site":"https://arcbounty.app","chain":5042,"adapter":"0x73c617e808ED5c7Ca41413DFC6EE940dDcBb0b8D"},
 "base":{"site":"https://basebounty.app","chain":8453,"adapter":"0x32c215908a46Eb5D34e4E5146c99891eD3014Fee"},
}
ALLOWED={"/api/v1/stats","/api/v1/bounties?status=open","/api/v1/bounties?status=paid"}
MAX_ROWS=150

def safe_get(site,path):
    if site not in {n["site"] for n in NETWORKS.values()} or path not in ALLOWED:
        raise ValueError("Unauthorised request blocked")
    req=urllib.request.Request(site+path,headers={
        "Accept":"application/json","User-Agent":"ProtocolPublicEscrowReadonly/1.0"},method="GET")
    with urllib.request.urlopen(req,timeout=22) as r:data=json.load(r)
    if not isinstance(data,dict):raise ValueError("Bad JSON response")
    return data

def decimal_or_none(value):
    try:
        n=Decimal(str(value))
        return n if n.is_finite() and n>=0 else None
    except (InvalidOperation,ValueError,TypeError):return None

def parse_open(cfg,data):
    if int(data.get("chainId",-1))!=cfg["chain"] or data.get("testnet") is not False:
        return {"status":"incomplete_wrong_network","claimed_chain":data.get("chainId"),
                "testnet":data.get("testnet")}
    tasks=data.get("bounties")
    if not isinstance(tasks,list):return {"status":"incomplete_schema","keys":list(data.keys())[:20]}
    rows=[]
    for t in tasks[:MAX_ROWS]:
        if not isinstance(t,dict):continue
        if t.get("status")!="open":continue
        reserved=t.get("reservedFor")
        reserved_flag=bool(reserved and str(reserved).lower()!="0x"+"0"*40)
        amount=decimal_or_none(t.get("rewardUsdc"))
        net=decimal_or_none(t.get("workerPayoutUsdc"))
        rows.append({"job_id":t.get("jobId"),"url":t.get("url"),
                     "gross_usdc":str(amount) if amount is not None else None,
                     "worker_net_before_gas_usdc":str(net) if net is not None else None,
                     "audience":t.get("audience"),"reserved":reserved_flag,
                     "bond_required":bool(t.get("workerBondRequired")),
                     "bond_usdc":t.get("workerBondUsdc"),"category":t.get("category"),
                     "deadline":t.get("deadline"),"description_ref":str(t.get("description") or "")[:90]})
    unreserved=[x for x in rows if not x["reserved"] and x["worker_net_before_gas_usdc"] is not None]
    high=[x for x in unreserved if Decimal(x["worker_net_before_gas_usdc"])>=25]
    return {"status":"mainnet_api_storage_snapshot_not_independent_payment_verification",
            "read_at":data.get("readAt"),"reported_count":data.get("count"),
            "open_count":len(rows),"unreserved_count":len(unreserved),
            "unreserved_worker_net_usdc_before_gas_total":str(sum(
                (Decimal(x["worker_net_before_gas_usdc"]) for x in unreserved),Decimal(0))),
            "unreserved_25plus_count":len(high),"high_tasks":high,
            "open_tasks":rows,"truncated":len(tasks)>MAX_ROWS,
            "warning":"Chain-storage-backed official API, NOT independent escrow proof. Confirm job instructions, ability, eligibility, history, currency liquidity, disputes and fees."}

def main():
    os.makedirs("reports",exist_ok=True)
    result={"utc":datetime.now(timezone.utc).isoformat(),
            "capital_spent_usd":0,"income_earned_usd":0,"networks":{}}
    for name,cfg in NETWORKS.items():
        out={"site":cfg["site"],"expected_chain":cfg["chain"],"canonical_adapter":cfg["adapter"]}
        for key,path in (("open","/api/v1/bounties?status=open"),
                         ("stats","/api/v1/stats"),("paid","/api/v1/bounties?status=paid")):
            try:
                obj=safe_get(cfg["site"],path)
                if key=="open":out[key]=parse_open(cfg,obj)
                elif int(obj.get("chainId",-1))!=cfg["chain"] or obj.get("testnet") is not False:
                    out[key]={"status":"incomplete_wrong_network"}
                elif key=="stats":
                    out[key]={"status":"reported_mainnet_stats",
                              "read_at":obj.get("readAt"),"posted":obj.get("posted"),
                              "open":obj.get("open"),"completed":obj.get("completed"),
                              "posted_usdc":obj.get("postedUsdc"),
                              "paid_to_workers_usdc":obj.get("paidToWorkersUsdc"),
                              "fee_bps":obj.get("feeBps")}
                else:
                    rows=obj.get("bounties",[])
                    out[key]={"status":"reported_mainnet_history","count":obj.get("count"),
                              "past_examples":[{"id":t.get("jobId"),"net_usdc":t.get("workerPayoutUsdc")}
                                               for t in rows[:12] if isinstance(t,dict)]}
            except Exception as e:
                out[key]={"status":"incomplete","error":str(e)[:240]}
        result["networks"][name]=out
    with open("reports/arc-base-live.json","w") as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
    return 0 if any(n["open"].get("status")=="mainnet_api_storage_snapshot_not_independent_payment_verification"
                    for n in result["networks"].values()) else 2
if __name__=="__main__":sys.exit(main())
