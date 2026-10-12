#!/usr/bin/env python3
"""Read-only Keep3r V2 mainnet funding census. NEVER sends, signs or claims funds."""
import json, os, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from eth_abi import encode,decode
from eth_utils import keccak

REGISTRY="0xeb02addCfD8B773A5FFA6B9d1FE99c566f8c44CC"
CHAIN_ID=1
PROVIDERS=("https://ethereum-rpc.publicnode.com","https://eth.llamarpc.com","https://eth.drpc.org")
TOKENS={
    "USDC":("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",6),
    "USDT":("0xdAC17F958D2ee523a2206206994597C13D831ec7",6),
    "DAI": ("0x6B175474E89094C44Da98b954EedeAC495271d0F",18),
    "WETH":("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",18),
}
ALLOWED={"eth_chainId","eth_getCode","eth_blockNumber","eth_call",
         "eth_getLogs","eth_getTransactionReceipt","eth_getTransactionByHash"}
MAX_JOBS=120

def selector(signature):
    return "0x"+keccak(text=signature)[:4].hex()

def rpc(url,method,params=()):
    if method not in ALLOWED:raise ValueError("Unauthorized or mutating RPC method: "+method)
    payload=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":list(params)}).encode()
    req=urllib.request.Request(url,data=payload,headers={"Content-Type":"application/json",
        "Accept":"application/json","User-Agent":"ProtocolKeep3rReadOnly/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=18) as response: item=json.load(response)
    except Exception as exc:raise RuntimeError(method+": "+str(exc)) from exc
    if "result" not in item or "error" in item:raise RuntimeError(method+": "+str(item.get("error","missing result")))
    return item["result"]

def view(url,signature,argtypes=None,values=None):
    raw=selector(signature)
    if argtypes:raw+=encode(argtypes,values).hex()
    answer=rpc(url,"eth_call",[{"to":REGISTRY,"data":raw},"latest"])
    if not isinstance(answer,str) or not answer.startswith("0x"):
        raise ValueError("RPC returned invalid eth_call bytes")
    return bytes.fromhex(answer[2:])

def uint(url,signature,types=None,params=None):
    return decode(["uint256"],view(url,signature,types,params))[0]

def scan(url):
    if int(rpc(url,"eth_chainId"),16)!=CHAIN_ID:raise RuntimeError("Wrong chain")
    code=rpc(url,"eth_getCode",[REGISTRY,"latest"])
    if not code or code in ("0x","0x0","0x00"):raise RuntimeError("No registry bytecode")
    tip=int(rpc(url,"eth_blockNumber"),16)
    alljobs=decode(["address[]"],view(url,"jobs()"))[0]
    rows=[]; errors=[]
    for job in alljobs[:MAX_JOBS]:
        row={"job":job,"liquidity_credits_raw":None,"worked_at":None,"token_credits":{}}
        try:
            row["liquidity_credits_raw"]=str(uint(url,"totalJobCredits(address)",["address"],[job]))
        except Exception as exc:errors.append({"job":job,"field":"totalJobCredits","error":str(exc)[:180]})
        try:
            row["worked_at"]=uint(url,"workedAt(address)",["address"],[job])
        except Exception as exc:errors.append({"job":job,"field":"workedAt","error":str(exc)[:180]})
        for name,(token,decimals) in TOKENS.items():
            try:
                raw=uint(url,"jobTokenCredits(address,address)",["address","address"],[job,token])
                if raw:
                    row["token_credits"][name]={"raw":str(raw),"units":str(Decimal(raw)/Decimal(10**decimals))}
            except Exception as exc:
                errors.append({"job":job,"field":"jobTokenCredits:"+name,"error":str(exc)[:180]})
        rows.append(row)
    withfunds=[r for r in rows if int(r["liquidity_credits_raw"] or 0)>0 or r["token_credits"]]
    incomplete=len(alljobs)>MAX_JOBS or bool(errors)
    return {
       "status":"partial_funding_observation" if incomplete else "funding_observation_not_claimability",
       "observed_utc":datetime.now(timezone.utc).isoformat(),
       "chain_id":CHAIN_ID,"block_number":tip,"registry":REGISTRY,
       "registry_jobs_total":len(alljobs),"jobs_scanned":len(rows),"funded_jobs_in_scanned_set":len(withfunds),
       "funded_jobs":withfunds,"jobs":[r for r in rows if r not in withfunds][:15],
       "unread_jobs":max(0,len(alljobs)-len(rows)),"per_field_errors":errors[:50],
       "error_count":len(errors),
       "scope":"Read-only credits and historical workedAt timestamp for up to 120 official Keep3r V2 jobs. Credits are not personally available bounty. No actual workability, permission checks, new entrant qualifications, gas estimates, payout conversion or recent receipt reconstruction.",
       "capital_spent_usd":0,"verified_income_usd":0,
    }

def main():
    os.makedirs("keep3r_reports",exist_ok=True)
    attempts=[]; report=None
    for provider in PROVIDERS:
        try:
            report=scan(provider)
            report["provider"]=provider
            attempts.append({"provider":provider,"status":report["status"]})
            break
        except Exception as exc:
            attempts.append({"provider":provider,"status":"incomplete","error":str(exc)[:280]})
    if report is None:report={"status":"incomplete","message":"No provider completed the job census. Not zero funding."}
    report["attempts"]=attempts
    with open("keep3r_reports/report.json","w") as f:json.dump(report,f,indent=2)
    print(json.dumps({"status":report["status"],"registry_jobs_total":report.get("registry_jobs_total"),
                      "jobs_scanned":report.get("jobs_scanned"),
                      "funded_jobs_in_scanned_set":report.get("funded_jobs_in_scanned_set"),
                      "funded_jobs":report.get("funded_jobs",[])[:10],
                      "error_count":report.get("error_count"),"attempts":attempts},indent=2))
    return 0 if report["status"]!="incomplete" else 2

if __name__=="__main__":sys.exit(main())
