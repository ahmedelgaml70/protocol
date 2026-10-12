#!/usr/bin/env python3
"""Ripe Protocol Base read-only keeper payout audit.

Checks current official manifest addresses for live code. Historical events
are collected by bounded eth_getLogs, with an optional free explorer fallback.
Only verified receipt logs can establish GREEN/sGREEN actually credited to
the caller. No signing, broadcasting, liquidation, token prices or spending.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request

from kerf_radar import JSONRPC, RPCError, words
from block_range import start_block_for_hours
from superfluid_receipts import TRANSFER

CHAIN_ID=8453
RPC_URL="https://mainnet.base.org"
TELLER="0xae87deB25Bc5030991Aa5E27Cbab38f37a112C13"
AUCTION="0xe9Dc24Ab1dC4746C7A43FAce3f895D9176D4C235"
GREEN="0xd1Eac76497D06Cf15475A5e3984D5bC03de7C707"
SGREEN="0xaa0f13488CE069A7B5a099457c753A7CFBE04d36"
MISSION="0x559E53F42b68b4995732Dba4aF300796761DBC19"
TOPIC="0x2ad3b92c465bc7ea1f27bef4120c0dee3b47cb039ba2af1c17061d831a465d2b"
ZERO="0x"+"0"*40
EXPLORER="https://base.blockscout.com/api/v2/addresses/"+AUCTION+"/logs"
TXHASH=re.compile(r"^0x[0-9a-fA-F]{64}$")


def address(n):
    if not 0<=n<2**160:
        raise ValueError("Invalid indexed address")
    return "0x"+f"{n:040x}"


def chain_state(rpc):
    chain=int(rpc.rpc("eth_chainId",[]),16)
    if chain!=CHAIN_ID:
        raise RPCError("Wrong network; expected Base 8453")
    tip=int(rpc.rpc("eth_blockNumber",[]),16)
    contracts={}
    for name,contract in (("Teller",TELLER),("AuctionHouse",AUCTION),
                          ("GreenToken",GREEN),("SavingsGreen",SGREEN),("MissionControl",MISSION)):
        code=rpc.rpc("eth_getCode",[contract,hex(tip)])
        if not isinstance(code,str) or code in ("0x","0x0",""):
            raise ValueError(f"{name} has no deployed bytecode at manifest address")
        contracts[name]={"address":contract,"code_present":True,
                         "code_bytes":len(code[2:])//2}
    return {"chain_id":chain,"tip_block":tip,
            "contracts":contracts,"source":"Ripe official Base mainnet v1 current manifest",
            "source_url":"https://github.com/Ripe-Foundation/ripe-protocol/blob/master/migration_history/base-mainnet/v1/current-manifest.json",
            "bytecode_matches_source_verified":False,
            "current_keeper_payout_verified":False,
            "transactions_sent":0}


def decode_liquidation(log):
    if str(log.get("address","")).lower()!=AUCTION.lower():
        raise ValueError("Wrong AuctionHouse log address")
    topics=log.get("topics",[])
    if len(topics)!=2 or topics[0].lower()!=TOPIC:
        raise ValueError("Unexpected LiquidateUser event topic")
    data=words(log["data"])
    if len(data)!=8 or data[3] not in (0,1):
        raise ValueError("Malformed LiquidateUser event ABI")
    h=log.get("transactionHash") or log.get("transaction_hash")
    if not isinstance(h,str) or not TXHASH.fullmatch(h):
        raise ValueError("Invalid log transaction hash")
    bn=log.get("blockNumber",log.get("block_number"))
    block_number=int(bn,16) if isinstance(bn,str) and bn.startswith("0x") else int(bn)
    return {"tx_hash":h.lower(),"block_number":block_number,
            "liquidated_user":address(int(topics[1],16)),
            "keeper_fee_raw":str(data[7]),
            "repay_amount_raw":str(data[2]),
            "created_auctions":data[6],
            "restored_debt_health":bool(data[3])}


def rpc_logs(rpc,start,end,chunk):
    out=[]
    for a in range(start,end+1,chunk):
        b=min(end,a+chunk-1)
        logs=rpc.rpc("eth_getLogs",[{"address":AUCTION,"fromBlock":hex(a),
                                   "toBlock":hex(b),"topics":[TOPIC]}])
        if not isinstance(logs,list):
            raise ValueError("Expected list from eth_getLogs")
        out.extend(decode_liquidation(x) for x in logs)
    return out,False,{"source":"eth_getLogs","blocks_covered":end-start+1}


def explorer_logs(start,end,max_pages=5):
    """Best-effort optional public Blockscout site; never infer zero on errors."""
    found=[]
    params={}
    exhausted=False
    for page in range(max_pages):
        query=urllib.parse.urlencode(params)
        url=EXPLORER+("?"+query if query else "")
        req=urllib.request.Request(url,headers={"Accept":"application/json",
                                "User-Agent":"protocol-ripe-research/1.0"})
        with urllib.request.urlopen(req,timeout=18) as f:
            data=json.load(f)
        if not isinstance(data,dict) or not isinstance(data.get("items"),list):
            raise ValueError("Unexpected free explorer response or API unavailable")
        for item in data["items"]:
            if not isinstance(item,dict):
                raise ValueError("Malformed explorer log")
            number=int(item.get("block_number",0))
            if number<start:
                exhausted=True
                break
            if number>end:
                continue
            if str(item.get("address",{})) and isinstance(item.get("address"),dict):
                item={**item,"address":item["address"].get("hash","")}
            if item.get("topics") and item["topics"][0].lower()==TOPIC:
                found.append(decode_liquidation(item))
        if exhausted:
            break
        next_page=data.get("next_page_params")
        if next_page is None:
            exhausted=True
            break
        if not isinstance(next_page,dict):
            raise ValueError("Malformed explorer pagination")
        params={k:str(v) for k,v in next_page.items() if v is not None}
    return found,not exhausted,{"source":"free explorer","pages_checked":page+1,
                                 "may_be_truncated":not exhausted}


def transfer_rows(receipt,sender):
    incoming_green,incoming_sgreen=0,0
    green_mint,sgreen_mint=0,0
    for log in receipt.get("logs",[]):
        token=str(log.get("address","")).lower()
        if token not in (GREEN.lower(),SGREEN.lower()):
            continue
        topics=log.get("topics",[])
        if len(topics)!=3 or topics[0].lower()!=TRANSFER:
            continue
        from_addr=address(int(topics[1],16))
        dest=address(int(topics[2],16))
        data=words(log["data"])
        if len(data)!=1:
            continue
        raw=data[0]
        if dest.lower()!=sender.lower():
            continue
        if token==GREEN.lower():
            incoming_green+=raw
            if from_addr==ZERO:
                green_mint+=raw
        else:
            incoming_sgreen+=raw
            if from_addr==ZERO:
                sgreen_mint+=raw
    return {"green_received_raw":str(incoming_green),
            "savings_green_shares_received_raw":str(incoming_sgreen),
            "green_direct_mint_raw":str(green_mint),
            "savings_green_shares_direct_mint_raw":str(sgreen_mint)}


def verify_transaction(rpc,hash_value,events):
    tx=rpc.rpc("eth_getTransactionByHash",[hash_value])
    receipt=rpc.rpc("eth_getTransactionReceipt",[hash_value])
    if not isinstance(tx,dict) or not isinstance(receipt,dict):
        raise ValueError("Transaction or receipt missing")
    if tx.get("hash","").lower()!=hash_value or int(receipt.get("status","0x0"),16)!=1:
        raise ValueError("No successful receipt for indexed liquidation")
    receipt_events=[]
    for log in receipt.get("logs",[]):
        topics=log.get("topics",[])
        if log.get("address","").lower()==AUCTION.lower() and topics and topics[0].lower()==TOPIC:
            receipt_events.append(decode_liquidation(log))
    if not receipt_events:
        raise ValueError("Explorer/RPC liquidate event not present in receipt")
    sender=tx["from"].lower()
    amounts=transfer_rows(receipt,sender)
    l2fee=int(receipt["gasUsed"],16)*int(receipt["effectiveGasPrice"],16)
    l1fee=int(receipt["l1Fee"],16) if receipt.get("l1Fee") is not None else None
    direct=tx.get("to","").lower()==TELLER.lower() if tx.get("to") else False
    positive=sum(int(x["keeper_fee_raw"]) for x in receipt_events)
    return {"tx_hash":hash_value,"submitter":sender,
            "tx_to":(tx.get("to") or "").lower(),
            "sent_directly_to_teller":direct,
            "successful":True,"liquidation_event_count":len(receipt_events),
            "indexed_positive_keeper_fee_raw":str(positive),
            "full_receipt_fee_wei":str(l2fee+l1fee) if l1fee is not None else None,
            **amounts,
            "actual_payout_to_submitter_observed":int(amounts["green_received_raw"])>0 or int(amounts["savings_green_shares_received_raw"])>0,
            "warning":"GREEN and sGREEN ERC4626 share units are NOT interchangeable or USD; fees are ETH, exits and gas losses unverified."}


def inspect(rpc,hours=6,chunk=1500,max_pages=5,receipt_limit=8):
    state=chain_state(rpc)
    tip=state["tip_block"]
    since=start_block_for_hours(rpc,tip,max(0,tip-60000),hours)
    source_error=None
    try:
        rows,truncated,coverage=rpc_logs(rpc,since,tip,chunk)
    except (OSError,RPCError,ValueError,TypeError) as e:
        source_error=type(e).__name__+": "+str(e)[:120]
        try:
            rows,truncated,coverage=explorer_logs(since,tip,max_pages)
        except (OSError,ValueError,TypeError,KeyError) as ex:
            return {**state,"from_block":since,
                    "history_status":"incomplete","history_event_count":None,
                    "primary_rpc_error":source_error,
                    "fallback_explorer_error":type(ex).__name__+": "+str(ex)[:120],
                    "verified_receipts":[],"no_activity_proven":False}
    dedup={}
    for item in rows:
        key=(item["tx_hash"],item["liquidated_user"])
        dedup[key]=item
    found=list(dedup.values())
    totals=Counter()
    for x in found:
        totals["keeper_fee_positive"]+=int(x["keeper_fee_raw"])>0
        totals["keeper_fee_zero"]+=int(x["keeper_fee_raw"])==0
    txgroups={}
    for x in found:
        txgroups.setdefault(x["tx_hash"],[]).append(x)
    hashes=sorted(txgroups,key=lambda k:(-sum(int(x["keeper_fee_raw"]) for x in txgroups[k]),k))[:receipt_limit]
    receipts=[]
    errors=[]
    for h in hashes:
        try:
            receipts.append(verify_transaction(rpc,h,txgroups[h]))
        except (RPCError,ValueError,TypeError,KeyError) as e:
            errors.append({"tx_hash":h,"error":type(e).__name__})
    return {**state,"from_block":since,"history_status":"partial" if truncated else "complete",
            "history_source":coverage,"initial_rpc_failure":source_error,
            "history_event_count":len(found),
            "positive_keeper_fee_event_count":totals["keeper_fee_positive"],
            "zero_keeper_fee_event_count":totals["keeper_fee_zero"],
            "unique_liquidation_transactions":len(txgroups),
            "receipt_samples":receipts,"receipt_errors":errors,
            "all_positive_payouts_proven":False,
            "current_eligible_liquidations_verified":False,
            "realized_usd_profit_verified":False,
            "note":"Historical successful calls already executed. Absence from a short/partial period is not proof of inactivity."}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rpc",default=RPC_URL)
    p.add_argument("--check",choices=("deployment","history"),default="history")
    p.add_argument("--hours",type=float,default=6)
    p.add_argument("--chunk",type=int,default=1500)
    p.add_argument("--pages",type=int,default=5)
    p.add_argument("--receipt-limit",type=int,default=8)
    p.add_argument("--output",default="ripe_base.json")
    a=p.parse_args(argv)
    if not (0<a.hours<=72 and 100<=a.chunk<=5000 and 1<=a.pages<=10 and 0<=a.receipt_limit<=30):
        p.error("Invalid window/chunk/pages/receipt-limit")
    try:
        rpc=JSONRPC(a.rpc)
        out=chain_state(rpc) if a.check=="deployment" else inspect(rpc,a.hours,a.chunk,a.pages,a.receipt_limit)
        path=Path(a.output)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    except (RPCError,ValueError,OSError,TypeError,KeyError) as e:
        print("RIPE READ-ONLY SCAN FAILED:",type(e).__name__,str(e)[:150],file=sys.stderr)
        return 2
    print("Base code verified at",out["tip_block"],"history status:",out.get("history_status","deployment-only"),
          "events:",out.get("history_event_count","not checked"))
    print("READ ONLY; no transaction sent. Output:",a.output)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
