#!/usr/bin/env python3
"""Read-only Morpho Blue Base API-event receipt integrity audit.

Verifies official indexed Liquidate events against successful Base tx receipts:
market id, event log index, liquidator/caller, repaid and seized raw tokens.
A token seizure is not USD profit; this module never transacts or signs.
"""
import argparse
import json
from pathlib import Path
import re
import sys

from kerf_radar import JSONRPC, RPCError, words

MORPHO = "0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb"
TOPIC = "0xa4946ede45d0c6f06a0f5ce92c9ad3b4751452d2fe0e25010783bcab57a67e41"
TXHASH = re.compile(r"^0x[0-9a-fA-F]{64}$")


def address_from_topic(s):
    n=int(s,16)
    if not 0<=n<2**160:
        raise ValueError("Bad padded address topic")
    return "0x"+f"{n:040x}"


def verify_one(rpc, tx_hash, indexed_events):
    tx=rpc.rpc("eth_getTransactionByHash",[tx_hash])
    receipt=rpc.rpc("eth_getTransactionReceipt",[tx_hash])
    if not isinstance(tx,dict) or not isinstance(receipt,dict):
        raise ValueError("Missing transaction or receipt")
    if tx.get("hash","").lower()!=tx_hash.lower() or int(receipt.get("status","0x0"),16)!=1:
        raise ValueError("API hash mismatch or reverted transaction")
    logs={int(x["logIndex"],16):x for x in receipt.get("logs",[])
          if isinstance(x.get("logIndex"),str)}
    matches=[]
    for e in indexed_events:
        log=logs.get(int(e["log_index"]))
        if log is None:
            raise ValueError("Indexed liquidation logIndex missing in receipt")
        ts=log.get("topics",[])
        if log.get("address","").lower()!=MORPHO.lower() or len(ts)!=4 or ts[0].lower()!=TOPIC:
            raise ValueError("Not the official Base Morpho Blue Liquidate event")
        values=words(log.get("data","0x"))
        if len(values)!=5:
            raise ValueError("Unexpected Morpho Liquidate event ABI")
        if (ts[1].lower()!=e["market_id"].lower()
            or address_from_topic(ts[2]).lower()!=e["indexed_liquidator"].lower()
            or str(values[0])!=e["repaidAssets_raw"]
            or str(values[2])!=e["seizedAssets_raw"]
            or str(values[3])!=e["badDebtAssets_raw"]):
            raise ValueError("Indexed raw economics differ from actual receipt")
        matches.append({
            "log_index":int(e["log_index"]),
            "market_id":e["market_id"],
            "indexed_liquidator":e["indexed_liquidator"],
            "liquidated_borrower":address_from_topic(ts[3]),
            "repaid_raw":str(values[0]),"seized_raw":str(values[2]),
            "bad_debt_raw":str(values[3]),
        })
    gas_l2=int(receipt["gasUsed"],16)*int(receipt["effectiveGasPrice"],16)
    l1=int(receipt["l1Fee"],16) if receipt.get("l1Fee") is not None else None
    return {"tx_hash":tx_hash.lower(),"successful":True,
            "tx_submitter":tx["from"].lower(),
            "tx_destination":(tx.get("to") or "").lower(),
            "full_gas_wei":str(gas_l2+l1) if l1 is not None else None,
            "l1_fee_available":l1 is not None,
            "validated_liquidation_events":matches,
            "onchain_liquidator_may_differ_from_tx_submitter":any(
                x["indexed_liquidator"].lower()!=tx["from"].lower() for x in matches),
            "actual_net_profit_usd_verified":False}


def audit(rpc, report, limit=8):
    if report.get("chain_id")!=8453:
        raise ValueError("Expected Base Morpho index")
    if int(rpc.rpc("eth_chainId",[]),16)!=8453:
        raise RPCError("Wrong RPC chain")
    events=report.get("events")
    if not isinstance(events,list) or not 1<=limit<=30:
        raise ValueError("Invalid event sample or limit")
    groups={}
    for e in events:
        if not isinstance(e,dict):
            raise ValueError("Malformed indexed event")
        h=str(e.get("tx_hash",""))
        if not TXHASH.fullmatch(h):
            raise ValueError("Malformed indexed tx hash")
        groups.setdefault(h.lower(),[]).append(e)
    chosen=list(groups)[:limit]
    out=[]; errors=[]
    for h in chosen:
        try:
            out.append(verify_one(rpc,h,groups[h]))
        except (RPCError,ValueError,TypeError,KeyError) as exc:
            errors.append({"hash":h,"kind":type(exc).__name__,"detail":str(exc)[:130]})
    return {"chain_id":8453,"official_morpho_contract":MORPHO,
            "source":"Official Morpho indexed GraphQL records cross-checked with Base receipts",
            "distinct_indexed_transactions":len(groups),
            "selected_tx_count":len(chosen),
            "validated_tx_count":len(out),"receipt_errors":errors,
            "rows":out,"transactions_sent":0,"realized_usd_profit_verified":False,
            "warning":"Verifies transaction integrity and gas only. No USD token-pricing, sell route, flash-loan/DEX cost, contention, failed attempts, or currently liquidatable account."
           }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--activity",default="reports/morpho_base_activity.json")
    p.add_argument("--rpc",default="https://mainnet.base.org")
    p.add_argument("--limit",type=int,default=8)
    p.add_argument("--output",default="reports/morpho_base_receipts.json")
    a=p.parse_args(argv)
    try:
        obj=json.loads(Path(a.activity).read_text(encoding="utf-8"))
        out=audit(JSONRPC(a.rpc),obj,a.limit)
        if out["receipt_errors"]:
            print("MORPHO RECEIPT AUDIT INCOMPLETE:",out["receipt_errors"][:2],file=sys.stderr)
            return 2
        Path(a.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    except (OSError,ValueError,TypeError,KeyError,RPCError) as exc:
        print("MORPHO RECEIPT AUDIT FAILED:",type(exc).__name__,str(exc)[:130],file=sys.stderr)
        return 2
    print("Indexed transactions verified:",out["validated_tx_count"],
          "events:",sum(len(x["validated_liquidation_events"]) for x in out["rows"]))
    print("READ ONLY. Never interpreted as USD profit.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
