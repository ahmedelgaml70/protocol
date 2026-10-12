#!/usr/bin/env python3
"""Ethereum Liquity V1 + current V2 liquidation compensation: READ-ONLY research."""
import json, os, sys, time, urllib.request
from datetime import datetime,timezone
from decimal import Decimal
from eth_abi import decode,encode
from eth_utils import keccak

RPCS=("https://ethereum-rpc.publicnode.com","https://eth.llamarpc.com",
      "https://eth.drpc.org","https://cloudflare-eth.com")
ALLOWED={"eth_chainId","eth_blockNumber","eth_getCode","eth_call","eth_getLogs",
         "eth_getTransactionReceipt","eth_getTransactionByHash","eth_gasPrice"}
DUMMY="0x1111111111111111111111111111111111111111"
ZERO="0x"+"0"*40
WETH="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
LUSD="0x5f98805A4E8be255a32880FDeC7F6728C6568bA0"
V1_TM="0xA39739EF8b0231DbFA0DcdA07d7e29faAbCf4bb2"
V1_SORTED="0x8FdD3fbFEb32b28fb73555518f8b361bCeA741A6"
V1_PRICE="0x4c517D4e2C851CA76d7eC94B805269Df0f2201De"
SCOPE={
 "v1_eth":{"manager":V1_TM,"fee_token":LUSD,"event":"Liquidation(uint256,uint256,uint256,uint256)","field_count":4},
 "v2_eth":{"manager":"0x7bcb64b2c9206a5b699ed43363f6f98d4776cf5a","fee_token":WETH,"event":"Liquidation("+",".join(["uint256"]*10)+")","field_count":10},
 "v2_wsteth":{"manager":"0xa2895d6a3bf110561dfe4b71ca539d84e1928b22","fee_token":WETH,"event":"Liquidation("+",".join(["uint256"]*10)+")","field_count":10},
 "v2_reth":{"manager":"0xb2b2abeb5c357a234363ff5d180912d319e3e19e","fee_token":WETH,"event":"Liquidation("+",".join(["uint256"]*10)+")","field_count":10},
}
TRANSFER_TOPIC="0x"+keccak(text="Transfer(address,address,uint256)").hex()
MAX_RECEIPTS=16
WINDOW_BLOCKS=52000  # approximately seven days; block range is recorded
CHUNK=500

def sig(text):
    return "0x"+keccak(text=text)[:4].hex()

def topic(text):
    return "0x"+keccak(text=text).hex()

def rpc(url,method,params=()):
    if method not in ALLOWED: raise ValueError("Unsupported/mutating RPC blocked: "+method)
    data=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":list(params)}).encode()
    req=urllib.request.Request(url,data=data,headers={"Content-Type":"application/json",
        "User-Agent":"ProtocolReadOnlyLiquity/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=16) as r: body=json.load(r)
    except Exception as e:
        raise RuntimeError(method+": "+str(e)) from e
    if "error" in body or "result" not in body:
        raise RuntimeError(method+": "+str(body.get("error","missing result")))
    return body["result"]

def ethcall(url,to,method,values=None,types=None):
    args=encode(types,values) if values is not None else b""
    return bytes.fromhex(rpc(url,"eth_call",[{"to":to,"data":sig(method)+args.hex()},"latest"])[2:])

def logs(url,address,topic0,begin,tip):
    rows=[]
    for n in range(begin,tip+1,CHUNK):
        r=rpc(url,"eth_getLogs",[{"address":address,
            "topics":[topic0],"fromBlock":hex(n),"toBlock":hex(min(n+CHUNK-1,tip))}])
        rows.extend(x for x in r if not x.get("removed",False))
    return rows

def event_info(key,log):
    scope=SCOPE[key]
    raw=bytes.fromhex(log["data"][2:])
    if len(raw)!=32*scope["field_count"]:raise ValueError("Event data length mismatch")
    nums=decode(["uint256"]*scope["field_count"],raw)
    if key=="v1_eth":
        fee_amount=nums[3]
        collateral_comp=nums[2]
    else:
        fee_amount=nums[2]
        collateral_comp=nums[3]
    return {"contract":key,"transaction_hash":log["transactionHash"],
            "block_number":int(log["blockNumber"],16),"raw_fee_token_compensation":str(fee_amount),
            "fee_token":scope["fee_token"],
            "fee_token_units":str(Decimal(fee_amount)/Decimal(10**18)),
            "raw_collateral_compensation":str(collateral_comp),
            "collateral_compensation_token_units":str(Decimal(collateral_comp)/Decimal(10**18))}

def receipt_check(url,item):
    tx=rpc(url,"eth_getTransactionByHash",[item["transaction_hash"]])
    rec=rpc(url,"eth_getTransactionReceipt",[item["transaction_hash"]])
    if not tx or not rec:raise ValueError("Transaction or receipt missing")
    if int(rec.get("status","0x0"),16)!=1:raise ValueError("Historical transaction failed")
    sender=tx["from"].lower()
    direct_sender_fee=0
    matching_token_transfers=[]
    for log in rec.get("logs",[]):
        tops=log.get("topics",[])
        if len(tops)<3 or tops[0].lower()!=TRANSFER_TOPIC:
            continue
        if log["address"].lower()!=item["fee_token"].lower():continue
        recipient="0x"+tops[2][-40:]
        amount=int(log["data"],16)
        matching_token_transfers.append({"recipient":recipient,"amount_raw":str(amount)})
        if recipient.lower()==sender:
            direct_sender_fee+=amount
    gas=int(rec["gasUsed"],16)*int(rec["effectiveGasPrice"],16)
    # Receipt gas includes L1 fee for some L2s, but Ethereum is L1 only.
    item["receipt"]={
        "transaction_sender":tx["from"],
        "transaction_destination":tx.get("to"),
        "gas_paid_eth":str(Decimal(gas)/Decimal(10**18)),
        "direct_fee_token_to_sender_units":str(Decimal(direct_sender_fee)/Decimal(10**18)),
        "fee_token_transfer_count":len(matching_token_transfers),
        "token_transfers":matching_token_transfers[:16],
        "caveat":"Fees may go to intermediary contracts; event amount is not realized caller profit."}
    return item

def historical(url,tip):
    begin=max(0,tip-WINDOW_BLOCKS+1)
    output=[]
    checked=0
    for key,scope in SCOPE.items():
        try:
            code=rpc(url,"eth_getCode",[scope["manager"],"latest"])
            if code in ("0x","0x0","0x00"):
                raise ValueError("No deployed bytecode at official address")
            rows=logs(url,scope["manager"],topic(scope["event"]),begin,tip)
            items=[]
            for row in rows:
                val=event_info(key,row)
                if checked<MAX_RECEIPTS:
                    try:receipt_check(url,val)
                    except Exception as e:val["receipt"]={"status":"incomplete","error":str(e)[:220]}
                    checked+=1
                else:val["receipt"]={"status":"not_checked_receipt_cap"}
                items.append(val)
            output.append({"name":key,"status":"success","events":len(items),
                           "sample_receipts":items[:50],
                           "results_truncated":len(items)>50})
        except Exception as e:
            output.append({"name":key,"status":"incomplete","error":str(e)[:250]})
    return {"block_from":begin,"block_to":tip,"branches":output,
            "successful_branches":sum(x["status"]=="success" for x in output),
            "incomplete_branches":sum(x["status"]!="success" for x in output)}

def v1_near_liquidations(url):
    output={"status":"incomplete","reviewed":0,"candidates":[],"note":
        "Only lowest nominal-collateral-ratio troves; not exhaustive. A successful eth_call can become stale before execution."}
    try:
        price=int.from_bytes(ethcall(url,V1_PRICE,"fetchPrice()"),"big")
        mcr=int.from_bytes(ethcall(url,V1_TM,"MCR()"),"big")
        tail=decode(["address"],ethcall(url,V1_SORTED,"getLast()"))[0]
        checked=[]
        for _ in range(12):
            if tail.lower()==ZERO.lower():break
            icr=int.from_bytes(ethcall(url,V1_TM,"getCurrentICR(address,uint256)",
                [tail,price],["address","uint256"]),"big")
            row={"trove":tail,"icr":str(icr),"mcr":str(mcr),
                 "below_mcr":icr<mcr,"liquidation_simulation":"not_run"}
            if icr<mcr:
                payload=sig("liquidate(address)")+encode(["address"],[tail]).hex()
                try:
                    rpc(url,"eth_call",[{"from":DUMMY,"to":V1_TM,"data":payload},"latest"])
                    row["liquidation_simulation"]="eth_call_success_not_execution_proof"
                    output["candidates"].append(row)
                except Exception as e:
                    row["liquidation_simulation"]="failed: "+str(e)[:150]
            checked.append(row)
            tail=decode(["address"],ethcall(url,V1_SORTED,"getPrev(address)",[tail],["address"]))[0]
        output.update({"status":"bounded_sample","price_usd_1e18":str(price),
                       "mcr_1e18":str(mcr),"reviewed":len(checked),"checked":checked})
    except Exception as e:output["error"]=str(e)[:300]
    return output

def main():
    os.makedirs("liquity_reports",exist_ok=True)
    attempts=[]
    for url in RPCS:
        try:
            if int(rpc(url,"eth_chainId"),16)!=1:raise RuntimeError("Wrong chain")
            tip=int(rpc(url,"eth_blockNumber"),16)
            history=historical(url,tip)
            live=v1_near_liquidations(url)
            if not history["successful_branches"] and live["status"]=="incomplete":
                raise RuntimeError("Historical and live screens both incomplete")
            result={"status":"partial_research_only" if history["incomplete_branches"]
                or live["status"]=="incomplete" else "sampled_research_only",
                "provider":url,"timestamp":datetime.now(timezone.utc).isoformat(),
                "ethereum_block":tip,"history":history,"v1_current_tail":live,
                "conclusion":"No earnings are established from a reward formula, historical transaction, or eth_call. Current candidates need further proof.",
                "capital_spent_usd":0,"realized_income_usd":0}
            attempts.append({"url":url,"status":result["status"]})
            break
        except Exception as e:
            attempts.append({"url":url,"status":"incomplete","error":str(e)[:240]})
    else:
        result={"status":"incomplete","message":"All RPCs failed; do not claim no rewards."}
    result["attempts"]=attempts
    with open("liquity_reports/report.json","w") as f:json.dump(result,f,indent=2)
    print(json.dumps({"status":result["status"],"attempts":attempts,
        "branch_counts":[{"name":b["name"],"events":b.get("events"),"status":b["status"]}
         for b in result.get("history",{}).get("branches",[])],
        "v1_live_status":result.get("v1_current_tail",{}).get("status"),
        "v1_candidate_count":len(result.get("v1_current_tail",{}).get("candidates",[]))},indent=2))
    return 0 if result["status"]!="incomplete" else 2

if __name__=="__main__":sys.exit(main())
