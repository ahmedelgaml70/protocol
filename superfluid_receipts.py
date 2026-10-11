#!/usr/bin/env python3
"""Read-only Base receipt evidence for Superfluid liquidator caller transfers.

Never signs, sends, approves or deposits. Inbound ERC20 transfers are not proof
of realized USD profit or eligibility for future rewards.
"""
import argparse
from decimal import Decimal
import json
import os
from pathlib import Path
import sys
import time
import urllib.request

CHAIN_ID = 8453
DEFAULT_RPC = "https://mainnet.base.org"
ETHX = "0x46fd5cfb4c12d87acd3a13e92baa53240c661d93"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
LIQUIDATION = "0xb8381a3ce157650e06186e3e8f4dd4dc29236f2688b6eed1893d0a60d7c6386f"
TXS = (
    "0x4688d1709a06a8adde20328eb9e71e3955ff1e54e64234073515bfff8b75668b",
    "0x8cf34f65aea1f5743fadd59e91036444744263a6ecd75e9b719c04a35bb7a709",
)
ALLOWED = {"eth_chainId", "eth_getTransactionByHash", "eth_getTransactionReceipt"}


class RPCError(RuntimeError):
    pass


def address(value):
    if not 0 <= value < 2 ** 160:
        raise ValueError("Invalid address")
    return "0x" + f"{value:040x}"


def words(blob):
    if not isinstance(blob, str) or not blob.startswith("0x"):
        raise ValueError("Malformed ABI payload")
    raw = bytes.fromhex(blob[2:])
    if len(raw) % 32:
        raise ValueError("Malformed ABI word size")
    return [int.from_bytes(raw[i:i+32], "big") for i in range(0, len(raw), 32)]


class RPC:
    """Only three permitted read-only JSON-RPC methods."""
    def __init__(self, url=DEFAULT_RPC, timeout=15, retries=2):
        if not url.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            raise ValueError("Use HTTPS or localhost RPC")
        self.url, self.timeout, self.retries, self.sequence = url, timeout, retries, 0

    def rpc(self, method, params):
        if method not in ALLOWED:
            raise RPCError(f"Disallowed receipt RPC method: {method}")
        self.sequence += 1
        payload = json.dumps({"jsonrpc": "2.0", "id": self.sequence,
                              "method": method, "params": params}).encode()
        req = urllib.request.Request(self.url, data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "protocol-receipts/0.1"})
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as stream:
                    result = json.load(stream)
                if not isinstance(result, dict) or "result" not in result:
                    raise RPCError(f"{method}: RPC error or missing result")
                return result["result"]
            except (OSError, TimeoutError, ValueError) as exc:
                if attempt == self.retries:
                    raise RPCError(f"{method}: connection failed ({type(exc).__name__})") from None
                time.sleep(min(2**attempt, 3))


def parse_receipt(tx, receipt):
    """Return inbound ETHx and fee evidence; never infer token price."""
    if tx is None or receipt is None:
        raise ValueError("Transaction or receipt missing; no opportunity inference")
    if int(receipt.get("status", "0x0"), 16) != 1:
        return {"tx_hash": tx["hash"], "status": "FAILED", "ethx_received_raw": "0",
                "liquidation_events": 0, "warning": "Failed call; gas may be lost"}
    sender = tx["from"].lower()
    inbound, matched, liq_count = 0, [], 0
    for log in receipt.get("logs", []):
        if log.get("address", "").lower() != ETHX.lower():
            continue
        topics = log.get("topics", [])
        if not topics:
            continue
        event = topics[0].lower()
        if event == LIQUIDATION:
            liq_count += 1
        if event != TRANSFER or len(topics) != 3:
            continue
        try:
            destination = address(int(topics[2], 16))
            source = address(int(topics[1], 16))
            values = words(log["data"])
            if len(values) != 1:
                continue
        except (ValueError, KeyError):
            continue
        if destination == sender:
            inbound += values[0]
            matched.append({"from": source, "amount_raw": str(values[0])})
    fee_l2 = int(receipt["gasUsed"], 16) * int(receipt["effectiveGasPrice"], 16)
    fee_l1 = int(receipt["l1Fee"], 16) if receipt.get("l1Fee") is not None else None
    fee_total = fee_l2 + fee_l1 if fee_l1 is not None else None
    return {
        "tx_hash": tx["hash"], "block_number": int(receipt["blockNumber"], 16),
        "status": "SUCCESS", "sender": sender, "ethx_token": ETHX,
        "liquidation_events": liq_count, "ethx_received_raw": str(inbound),
        "ethx_received_tokens": str(Decimal(inbound) / Decimal(10**18)),
        "inbound_transfers": matched, "l2_fee_wei": str(fee_l2),
        "l1_fee_wei": str(fee_l1) if fee_l1 is not None else None,
        "full_fee_wei": str(fee_total) if fee_total is not None else None,
        "completeness": "full_fee_available" if fee_total is not None else "L1_FEE_MISSING",
        "warning": "Inbound transfer is not proof of exclusive liquidation reward. No sale proceeds, swap costs or realized profits checked."
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rpc", default=os.environ.get("BASE_RPC_URL", DEFAULT_RPC))
    p.add_argument("--tx", action="append", help="Existing Base tx hash; may be repeated")
    p.add_argument("--output", default="superfluid_receipts.json")
    a = p.parse_args(argv)
    txs = a.tx or list(TXS)
    if any(len(h) != 66 or not h.startswith("0x") or
           any(c not in "0123456789abcdefABCDEF" for c in h[2:]) for h in txs):
        p.error("Requires full 0x-prefixed 32-byte transaction hashes")
    try:
        rpc = RPC(a.rpc)
        chain_id = int(rpc.rpc("eth_chainId", []), 16)
        if chain_id != CHAIN_ID:
            raise RPCError(f"Wrong chain {chain_id}; expected Base 8453")
        rows = [
            parse_receipt(rpc.rpc("eth_getTransactionByHash", [h]),
                          rpc.rpc("eth_getTransactionReceipt", [h]))
            for h in txs
        ]
    except (ValueError, RPCError) as exc:
        print(f"RECEIPT AUDIT FAILED: {exc}", file=sys.stderr)
        return 2
    data = {"chain_id": chain_id, "source": "read-only RPC receipts",
            "rows": rows, "transactions_sent": 0, "profit_usd_verified": False}
    Path(a.output).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(row["tx_hash"][:12], row["status"], "ETHx inbound:", row["ethx_received_raw"],
              "L1 fee:", row.get("l1_fee_wei"))
    print("READ ONLY. Output:", a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
