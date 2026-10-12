#!/usr/bin/env python3
"""Independent, read-only Base receipts for Beefy Cowllector reported harvests.

Counts actual Base WETH ERC20 movements to/from transaction submitter. Rewards
may be forwarded by contracts other than the strategy; these are token movements,
not a full portfolio P&L or proof the keeper fee was owed to outsiders.
Never signs, sends, approves, or deposits.
"""
import argparse
from decimal import Decimal
import json
from pathlib import Path
import sys

from superfluid_receipts import RPC, RPCError, TRANSFER, words

BASE_CHAIN_ID=8453
WETH="0x4200000000000000000000000000000000000006"


def addr(topic):
    if not isinstance(topic,str):
        raise ValueError("Bad indexed ERC20 address")
    n=int(topic,16)
    if n>>160:
        raise ValueError("Bad padded ERC20 address")
    return "0x"+f"{n:040x}"


def inspect_one(rpc, row):
    h=row["operator_tx_hash_unverified"].lower()
    strategy=row["strategy_address"].lower()
    if len(h)!=66 or not h.startswith("0x") or not all(c in "0123456789abcdef" for c in h[2:]):
        raise ValueError("Invalid transaction hash")
    if len(strategy)!=42 or not strategy.startswith("0x"):
        raise ValueError("Invalid strategy address")
    tx=rpc.rpc("eth_getTransactionByHash",[h])
    rec=rpc.rpc("eth_getTransactionReceipt",[h])
    if not isinstance(tx,dict) or not isinstance(rec,dict) or tx.get("hash","").lower()!=h:
        raise ValueError("Missing/mismatched transaction or receipt")
    sender=tx["from"].lower()
    to=(tx.get("to") or "").lower()
    incoming=0
    direct_strategy_incoming=0
    outgoing=0
    for log in rec.get("logs",[]):
        topics=log.get("topics",[])
        if log.get("address","").lower()!=WETH or len(topics)!=3 or topics[0].lower()!=TRANSFER:
            continue
        try:
            from_address=addr(topics[1])
            to_address=addr(topics[2])
            amount=words(log.get("data","0x"))
            if len(amount)!=1:
                continue
            amount=amount[0]
        except (KeyError,ValueError,TypeError):
            continue
        if to_address==sender:
            incoming+=amount
            if from_address==strategy:
                direct_strategy_incoming+=amount
        if from_address==sender:
            outgoing+=amount
    status=int(rec.get("status","0x0"),16)
    gas_l2=int(rec["gasUsed"],16)*int(rec["effectiveGasPrice"],16)
    gas_l1=int(rec["l1Fee"],16) if rec.get("l1Fee") is not None else None
    full_gas=(gas_l2+gas_l1) if gas_l1 is not None else None
    net=(incoming-outgoing-full_gas) if full_gas is not None and status==1 else None
    return {
        "transaction_hash":h,
        "strategy_address_expected":strategy,
        "destination_matches_strategy":to==strategy,
        "submitting_wallet":sender,
        "transaction_success":status==1,
        "weth_received_by_submitter_raw":str(incoming),
        "weth_sent_by_submitter_raw":str(outgoing),
        "weth_received_directly_from_strategy_raw":str(direct_strategy_incoming),
        "full_base_gas_fee_wei":str(full_gas) if full_gas is not None else None,
        "l1_fee_available":gas_l1 is not None,
        "conditional_weth_parity_after_gas_eth":str(Decimal(net)/(10**18)) if net is not None else None,
        "scope":"WETH receipts only; native ETH transfers, internal calls, other tokens, L1 data beyond receipt and actual exit price not verified"
    }


def scan(rpc, source, limit=12):
    if int(rpc.rpc("eth_chainId",[]),16)!=BASE_CHAIN_ID:
        raise RPCError("Wrong chain; expected Base mainnet 8453")
    sample=source.get("recent_operator_harvest_sample")
    if not isinstance(sample,list):
        raise ValueError("Beefy source missing harvested transaction sample")
    chosen=[]
    for e in sample:
        if isinstance(e,dict) and e.get("chain")=="base" and e.get("operator_transaction_ok") is True:
            if e["operator_tx_hash_unverified"].lower() not in {r["operator_tx_hash_unverified"].lower() for r in chosen}:
                chosen.append(e)
        if len(chosen)>=limit:
            break
    result=[]
    errors=[]
    for item in chosen:
        try:
            result.append(inspect_one(rpc,item))
        except (RPCError,ValueError,KeyError,TypeError) as exc:
            errors.append({"tx":item.get("operator_tx_hash_unverified"),"error":type(exc).__name__,"detail":str(exc)[:180]})
    return {"chain_id":BASE_CHAIN_ID,
            "evidence":"public Beefy Cowllector-v2 reports plus independently read-only Base receipts",
            "reported_base_harvest_txs_selected":len(chosen),
            "receipt_rows":result,"receipt_errors":errors,
            "successful_strategy_harvest_receipts":sum(r["transaction_success"] and r["destination_matches_strategy"] for r in result),
            "conditional_positive_wnative_after_gas_count":sum(
                r["conditional_weth_parity_after_gas_eth"] is not None
                and Decimal(r["conditional_weth_parity_after_gas_eth"])>0 for r in result),
            "wallet_transactions_sent":0,
            "actual_realized_usd_profit_verified":False,
            "warning":"These are past incumbent-operator harvest transactions, NOT open bounties. WETH-only receipt net proxy excludes internal ETH, other tokens, failed tries and conversions."}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--activity",default="reports/beefy_cowllector.json")
    p.add_argument("--rpc",default="https://base-rpc.publicnode.com")
    p.add_argument("--limit",type=int,default=10)
    p.add_argument("--output",default="reports/beefy_base_receipts.json")
    a=p.parse_args(argv)
    if not 1<=a.limit<=20:
        p.error("limit must be 1..20")
    try:
        report=json.loads(Path(a.activity).read_text(encoding="utf-8"))
        audited=scan(RPC(a.rpc),report,a.limit)
        if audited["receipt_errors"]:
            print("BEEFY RECEIPTS INCOMPLETE:",json.dumps(audited["receipt_errors"][:3]),file=sys.stderr)
            return 2
    except (OSError,ValueError,KeyError,RPCError) as exc:
        print("BEEFY RECEIPTS FAILED:",type(exc).__name__,str(exc)[:130],file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(audited,indent=2)+"\n",encoding="utf-8")
    print("Harvests inspected:",len(audited["receipt_rows"]),
          "conditional positive WETH after gas:",audited["conditional_positive_wnative_after_gas_count"])
    print("READ ONLY; no third-party future profits verified.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
