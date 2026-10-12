#!/usr/bin/env python3
"""Sovryn Zero Rootstock live liquidatable-position preflight; read-only."""
import json,os,sys
from datetime import datetime,timezone
from eth_abi import decode,encode
import liquity_compensation as helper

TM="0x82B09695ee4F214f3A0803683C4AaEc332E4E0a3"
SORTED="0xdeEB95480B94f9395514Fe35CAF692A1C788DfE9"
PRICE="0x6D1d9574d67e04cf35Fa1d916F763eDDae03b75d"
PARAMS="0xf8B04A36c36d5DbD1a9Fe7B74897c609d6A17aa2"
ZUSD="0xdB107FA69E33f05180a4C2cE9c2E7CB481645C2d"
PROVIDERS=("https://public-node.rsk.co","https://rootstock.drpc.org","https://mycrypto.rsk.co")
EVENT="Liquidation(uint256,uint256,uint256,uint256)"
ZERO="0x"+"0"*40
MAX_TROVES=12

def live_tail(url):
    price=int.from_bytes(helper.ethcall(url,PRICE,"fetchPrice()"),"big")
    mcr=int.from_bytes(helper.ethcall(url,PARAMS,"MCR()"),"big")
    current=decode(["address"],helper.ethcall(url,SORTED,"getLast()"))[0]
    found=[]; checked=[]
    for _ in range(MAX_TROVES):
        if current.lower()==ZERO.lower():break
        icr=int.from_bytes(helper.ethcall(url,TM,"getCurrentICR(address,uint256)",
            [current,price],["address","uint256"]),"big")
        info={"trove":current,"icr":str(icr),"mcr":str(mcr),"below_mcr":icr<mcr,
              "eth_call_liquidation":"not_eligible_for_probe"}
        if icr < mcr:
            try:
                data=helper.sig("liquidate(address)")+encode(["address"],[current]).hex()
                helper.rpc(url,"eth_call",[{"from":helper.DUMMY,"to":TM,"data":data},"latest"])
                info["eth_call_liquidation"]="success_not_execution_proof"
                found.append(info)
            except Exception as exc:
                info["eth_call_liquidation"]="failed:"+str(exc)[:150]
        checked.append(info)
        current=decode(["address"],helper.ethcall(url,SORTED,"getPrev(address)",
            [current],["address"]))[0]
    return {"status":"bounded_readonly","price_raw":str(price),"mcr_raw":str(mcr),
            "reviewed":len(checked),"checked":checked,"candidates":found,
            "note":"Tail scan is not exhaustive. Recovery Mode and pending redistributions can change eligibility."}

def audit(url):
    if int(helper.rpc(url,"eth_chainId"),16)!=30:raise RuntimeError("Wrong Rootstock chain")
    for addr in [TM,SORTED,PRICE,PARAMS,ZUSD]:
        if helper.rpc(url,"eth_getCode",[addr,"latest"]) in ("0x","0x0","0x00"):
            raise RuntimeError("No deployed code at "+addr)
    tip=int(helper.rpc(url,"eth_blockNumber"),16)
    helper.SCOPE.clear()
    helper.SCOPE["sovryn_zero"]={"manager":TM,"fee_token":ZUSD,
        "event":EVENT,"field_count":4}
    helper.WINDOW_BLOCKS=3400   # short recent bounded Rootstock history
    helper.CHUNK=300
    history=helper.historical(url,tip)
    try:current=live_tail(url)
    except Exception as exc:current={"status":"incomplete","error":str(exc)[:240]}
    return {"status":"sampled_research_only" if history["successful_branches"] and current["status"]!="incomplete"
        else "partial_research_only" if history["successful_branches"] or current["status"]!="incomplete" else "incomplete",
        "provider":url,"observed_at":datetime.now(timezone.utc).isoformat(),
        "chain_id":30,"tip":tip,"historical":history,"current_tail":current,
        "economic_note":"Formula 20 ZUSD + 0.5% RBTC in official Sovryn docs; does not prove profit or actual transferability, ZUSD price, competition or available position.",
        "money_spent_usd":0,"income_realized_usd":0}

def main():
    os.makedirs("sovryn_reports",exist_ok=True)
    errors=[]; result=None
    for url in PROVIDERS:
        try:
            result=audit(url)
            if result["status"]!="incomplete":break
        except Exception as exc:
            errors.append({"url":url,"error":str(exc)[:220]})
            result=None
    if result is None:result={"status":"incomplete"}
    result["provider_errors"]=errors
    with open("sovryn_reports/report.json","w") as f:json.dump(result,f,indent=2)
    print(json.dumps({"status":result["status"],"provider":result.get("provider"),
        "history": [{"name":x["name"],"events":x.get("events"),"status":x["status"],
                     "error":x.get("error")} for x in result.get("historical",{}).get("branches",[])],
        "live":result.get("current_tail",{}).get("status"),
        "current_candidates":len(result.get("current_tail",{}).get("candidates",[])),
        "errors":errors},indent=2))
    return 0 if result["status"]!="incomplete" else 2

if __name__=="__main__":sys.exit(main())
