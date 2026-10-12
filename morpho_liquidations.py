#!/usr/bin/env python3
"""Morpho Blue Base permissionless liquidation ACTIVITY research via official API.

No keys/wallets. Indexed transactions are historical executed actions; raw
collateral and debt amounts are incomparable until priced, and even positive
gross spreads do not prove profits, flash-liquidity access or open targets.
"""
import argparse
from collections import Counter
from decimal import Decimal, InvalidOperation, localcontext
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
import urllib.request

GRAPHQL = "https://api.morpho.org/graphql"
HASH = re.compile(r"^0x[0-9a-fA-F]{64}$")
ADDRESS = re.compile(r"^0x[0-9a-fA-F]{40}$")
QUERY = """query RecentBaseLiquidations($first:Int!){
 marketTransactions(first:$first,orderBy:Timestamp,orderDirection:Desc,
                    where:{chainId_in:[8453],type_in:[Liquidation]}){
   items {
     txHash timestamp blockNumber logIndex type
     market { marketId loanAsset { address symbol decimals priceUsd } collateralAsset { address symbol decimals priceUsd } }
     data { ... on MarketTransactionLiquidationData {
       repaidAssets seizedAssets badDebtAssets liquidator
     } }
   }
 }
}"""


def fetch(limit):
    request = urllib.request.Request(
        GRAPHQL, data=json.dumps({"query": QUERY, "variables": {"first": limit}}).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": "protocol-readonly-morpho-screen/1.0"},
    )
    with urllib.request.urlopen(request, timeout=25) as f:
        data=json.load(f)
    if not isinstance(data, dict) or data.get("errors"):
        raise ValueError("Morpho GraphQL rejected query or returned errors")
    results=data.get("data",{}).get("marketTransactions",{}).get("items")
    if not isinstance(results,list):
        raise ValueError("Morpho GraphQL missing marketTransactions.items")
    return results



def asset_info(value):
    """PriceUsd is a CURRENT reference, never historic realized proceeds."""
    if not isinstance(value, dict) or not ADDRESS.fullmatch(str(value.get("address", ""))):
        return None
    try:
        decimals = int(value["decimals"])
        price = Decimal(str(value["priceUsd"]))
        if not 0 <= decimals <= 36 or not price.is_finite() or not 0 < price < Decimal("1e12"):
            return None
    except (KeyError, ValueError, TypeError, InvalidOperation):
        return None
    return {
        "address": value["address"].lower(),
        "symbol": str(value.get("symbol") or "")[:32],
        "decimals": decimals,
        "current_reference_price_usd": str(price)
    }


def illustrative_valuation(debt, collateral, loan, collateral_token):
    """Potential gross spread at current reference prices, NOT historic profit."""
    if loan is None or collateral_token is None:
        return None
    with localcontext() as ctx:
        ctx.prec = 90
        debt_usd = (Decimal(debt) / (Decimal(10) ** loan["decimals"])
                    * Decimal(loan["current_reference_price_usd"]))
        seized_usd = (Decimal(collateral) / (Decimal(10) ** collateral_token["decimals"])
                      * Decimal(collateral_token["current_reference_price_usd"]))
    return {
        "repaid_debt_current_reference_usd": str(debt_usd),
        "seized_collateral_current_reference_usd": str(seized_usd),
        "gross_current_reference_spread_usd": str(seized_usd - debt_usd),
        "is_historical_realized_profit": False,
        "exit_price_and_liquidity_verified": False,
    }


def summarize(items, now, days, limit):
    if not isinstance(items,list) or not 1<=days<=30 or not 1<=limit<=500:
        raise ValueError("Invalid query boundaries")
    cutoff=int((now-timedelta(days=days)).timestamp())
    recents=[]
    seen=set()
    counts=Counter()
    valued_count=0
    positive_reference_spread=0
    for row in items:
        if not isinstance(row,dict) or row.get("type")!="Liquidation":
            raise ValueError("Unexpected non-liquidation record")
        tx=str(row.get("txHash",""))
        if not HASH.fullmatch(tx):
            raise ValueError("Invalid liquidation tx hash")
        raw=row.get("data")
        if not isinstance(raw,dict):
            raise ValueError("Missing liquidation data")
        who=str(raw.get("liquidator",""))
        if not ADDRESS.fullmatch(who):
            raise ValueError("Invalid indexed liquidator")
        market=row.get("market") or {}
        market_id=str(market.get("marketId",""))
        if not HASH.fullmatch(market_id):
            raise ValueError("Invalid indexed market id")
        stamp=int(row["timestamp"])
        if stamp>int(now.timestamp())+600:
            raise ValueError("Future liquidation event timestamp")
        values={}
        for k in ("repaidAssets","seizedAssets","badDebtAssets"):
            n=int(raw.get(k,0))
            if n<0:
                raise ValueError("Negative repayment/collateral")
            values[k+"_raw"]=str(n)
        if stamp<cutoff:
            continue
        loan = asset_info(market.get("loanAsset"))
        collateral_asset = asset_info(market.get("collateralAsset"))
        current_reference = illustrative_valuation(
            int(values["repaidAssets_raw"]),
            int(values["seizedAssets_raw"]), loan, collateral_asset
        )
        if current_reference is not None:
            valued_count += 1
            if Decimal(current_reference["gross_current_reference_spread_usd"]) > 0:
                positive_reference_spread += 1
        log_index=int(row["logIndex"])
        if log_index<0 or log_index>100000:
            raise ValueError("Unexpected event log index")
        key=(tx.lower(),market_id.lower(),log_index)
        if key in seen:
            continue
        seen.add(key)
        counts[who.lower()]+=1
        recents.append({
            "tx_hash":tx.lower(),"block_number":int(row["blockNumber"]),
            "log_index":log_index,
            "timestamp_utc":datetime.fromtimestamp(stamp,timezone.utc).isoformat(),
            "market_id":market_id.lower(),
            "indexed_liquidator":who.lower(),**values,
            "loan_asset_reference":loan,"collateral_asset_reference":collateral_asset,
            "indicative_current_reference_valuation":current_reference,
            "receipt_verified":False,"wallet_net_profit_verified":False,
        })
    return {
        "source":"Morpho official public GraphQL API",
        "endpoint":GRAPHQL,"chain_id":8453,"days_requested":days,
        "sample_limit":limit,"returned_indexed_events":len(items),
        "query_may_be_truncated":len(items)>=limit,
        "recent_liquidation_records":len(recents),
        "unique_transaction_hashes":len({r["tx_hash"] for r in recents}),
        "unique_indexed_liquidator_addresses":len(counts),
        "top_indexed_liquidator_event_count":counts.most_common(5),
        "latest_recent_transaction":recents[0]["tx_hash"] if recents else None,
        "oldest_observed_event_utc":recents[-1]["timestamp_utc"] if recents else None,
        "distinct_liquidation_event_identifiers":len(recents),
        "current_reference_valued_event_count":valued_count,
        "current_reference_positive_gross_spread_event_count":positive_reference_spread,
        "events":recents,
        "transactions_sent":0,"profit_usd_verified":False,
        "warning":"Gross spread uses CURRENT Morpho API reference prices, not transaction-time execution proceeds. No swap exit quotes, slippage, flash liquidity, failed-call gas, or historic realized PnL. Query may be capped."
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--days",type=int,default=7)
    p.add_argument("--limit",type=int,default=100)
    p.add_argument("--output",default="morpho_base_activity.json")
    args=p.parse_args(argv)
    if not 1<=args.days<=30 or not 1<=args.limit<=500:
        p.error("days 1..30 and limit 1..500")
    try:
        obj=summarize(fetch(args.limit),datetime.now(timezone.utc),args.days,args.limit)
        Path(args.output).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print("MORPHO INDEX SCAN FAILED:",type(exc).__name__,str(exc)[:130],file=sys.stderr)
        return 2
    print("Recent Base indexed liquidations:",obj["recent_liquidation_records"],
          "txs:",obj["unique_transaction_hashes"],
          "may be capped:",obj["query_may_be_truncated"])
    print("READ ONLY; no keeper payout or available profit proven.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
