#!/usr/bin/env python3
"""Read-only Kerf RangeOrders observer for Robinhood Chain.

Python 3.10+; standard library only. Never imports a wallet, signs, approves,
deploys or broadcasts a transaction. Estimates are NOT execution authorization.
"""
import argparse
from decimal import Decimal, localcontext
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request

CHAIN_ID = 4663
DEFAULT_RPC = "https://rpc.mainnet.chain.robinhood.com"
RANGE_ORDERS = "0xfE368De9fB4b0Ce845a7546B4261d4D15dC87C0C"
# Selectors correspond to published function signatures; verify against deployed ABI.
SELECTORS = {
    "nextOrderId()": "2a58b330",
    "orders(uint256)": "a85c38ef",
    "fillable(uint256)": "4f071557",
    "weth()": "3fc8cef3",
    "token0()": "0dfe1681",
    "token1()": "d21220a7",
    "decimals()": "313ce567",
    "symbol()": "95d89b41",
    "fill(uint256)": "3fda5389",
}
HEX_ADDRESS = re.compile(r"^0x[0-9a-fA-F]{40}$")


class RPCError(RuntimeError):
    pass


def calldata(signature, *args):
    if signature not in SELECTORS:
        raise ValueError("Unknown read-only/simulation selector")
    return "0x" + SELECTORS[signature] + "".join(f"{int(n):064x}" for n in args)


def words(blob):
    if not isinstance(blob, str) or not blob.startswith("0x"):
        raise ValueError("Invalid ABI result")
    raw = bytes.fromhex(blob[2:])
    if len(raw) % 32:
        raise ValueError("Invalid ABI word count")
    return [int.from_bytes(raw[i:i + 32], "big") for i in range(0, len(raw), 32)]


def address(n):
    if not 0 <= n < 2 ** 160:
        raise ValueError("Malformed ABI address")
    return "0x" + f"{n:040x}"


def signed(n, bits):
    n &= (1 << bits) - 1
    return n - (1 << bits) if n >= (1 << (bits - 1)) else n


class JSONRPC:
    def __init__(self, url=DEFAULT_RPC, timeout=15, retries=2):
        if not url.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            raise ValueError("Use an HTTPS RPC (or localhost)")
        self.url, self.timeout, self.retries = url, timeout, retries
        self.sequence = 0

    def rpc(self, method, params):
        # Never permit transaction submission methods through this client.
        if method not in {
            "eth_chainId", "eth_blockNumber", "eth_getCode", "eth_call",
            "eth_gasPrice", "eth_estimateGas", "eth_getLogs"
        }:
            raise RPCError(f"Disallowed RPC method: {method}")
        self.sequence += 1
        payload = json.dumps({
            "jsonrpc": "2.0", "id": self.sequence, "method": method, "params": params
        }).encode()
        req = urllib.request.Request(
            self.url, data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "protocol-read-only/0.2"}
        )
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as stream:
                    result = json.load(stream)
                if not isinstance(result, dict) or "result" not in result:
                    raise RPCError(f"{method} returned missing result: {str(result.get('error') if isinstance(result, dict) else 'invalid response')[:180]}")
                return result["result"]
            except (OSError, TimeoutError, ValueError) as exc:
                if isinstance(exc, RPCError):
                    raise
                if attempt == self.retries:
                    # Do not accidentally print RPC URLs containing API keys.
                    raise RPCError(f"{method}: RPC connection failed ({type(exc).__name__})") from None
                time.sleep(min(2 ** attempt, 3))
        raise RPCError(f"{method}: retry exhausted")

    def call(self, contract, data, block):
        return self.rpc("eth_call", [{"to": contract, "data": data}, block])

    def uint(self, contract, signature, block, *args):
        result = words(self.call(contract, calldata(signature, *args), block))
        if not result:
            raise RPCError(f"{signature}: empty return")
        return result[0]

    def estimate_gas(self, tx):
        return int(self.rpc("eth_estimateGas", [tx]), 16)


def decode_order(payload):
    fields = words(payload)
    if len(fields) != 10:
        raise ValueError(f"Unexpected order tuple length {len(fields)}; check deployed ABI")
    return {
        "owner": address(fields[0]),
        "token_id": fields[1],
        "pool": address(fields[2]),
        "zero_for_one": bool(fields[3]),
        "tick_lower": signed(fields[4], 24),
        "tick_upper": signed(fields[5], 24),
        "liquidity": fields[6],
        "amount_in": str(fields[7]),
        "placed_at": fields[8],
        "status": ("open", "filled", "cancelled")[fields[9]] if fields[9] in (0, 1, 2) else f"unknown-{fields[9]}"
    }


def token_info(rpc, token, block):
    decimals = rpc.uint(token, "decimals()", block)
    if decimals > 36:
        raise ValueError("Unexpected token decimal precision")
    symbol = token[:10]
    try:
        raw = bytes.fromhex(rpc.call(token, calldata("symbol()"), block)[2:])
        if len(raw) == 32:
            symbol = raw.rstrip(b"\x00").decode("utf-8", "replace") or symbol
        elif len(raw) >= 96:
            offset = int.from_bytes(raw[:32], "big")
            if offset + 32 <= len(raw):
                length = int.from_bytes(raw[offset:offset + 32], "big")
                if 0 < length <= 96 and offset + 32 + length <= len(raw):
                    symbol = raw[offset + 32:offset + 32 + length].decode("utf-8", "replace")
    except (ValueError, RPCError, UnicodeError):
        pass
    return {"address": token, "symbol": symbol, "decimals": decimals}


def estimated_principal(liquidity, tick_lower, tick_upper, zero_for_one):
    """Fully crossed Uniswap V3 principal only, not an exact payout simulation."""
    if not (-887272 <= tick_lower < tick_upper <= 887272):
        raise ValueError("Invalid Uniswap V3 tick range")
    with localcontext() as ctx:
        ctx.prec = 85
        lo = Decimal("1.0001") ** (Decimal(tick_lower) / 2)
        hi = Decimal("1.0001") ** (Decimal(tick_upper) / 2)
        diff = hi - lo
        amount = Decimal(liquidity) * (diff if zero_for_one else diff / (hi * lo))
    return max(0, int(amount))


def estimated_bounty_raw(liquidity, tick_lower, tick_upper, zero_for_one):
    return estimated_principal(liquidity, tick_lower, tick_upper, zero_for_one) // 100


def read_prices(path):
    if path is None:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Price JSON must be address -> USD decimal object")
    result = {}
    for k, v in data.items():
        if not HEX_ADDRESS.fullmatch(k):
            raise ValueError("Price key must be a token contract address")
        n = Decimal(str(v))
        if not n.is_finite() or n <= 0:
            raise ValueError("All supplied prices must be positive and finite")
        result[k.lower()] = n
    return result


def scan(rpc, max_orders=100, sim_from=None, prices=None, eth_usd=None,
         gas_multiplier=Decimal("1.5"), gas_ceiling=500000, min_profit_usd=Decimal("1")):
    prices = prices or {}
    chain = int(rpc.rpc("eth_chainId", []), 16)
    if chain != CHAIN_ID:
        raise RPCError(f"Wrong chain: {chain}; expected {CHAIN_ID}")
    block_number = int(rpc.rpc("eth_blockNumber", []), 16)
    block = hex(block_number)
    if rpc.rpc("eth_getCode", [RANGE_ORDERS, block]) in ("0x", None):
        raise RPCError("No code at published Kerf contract; verify deployment address")
    next_id = rpc.uint(RANGE_ORDERS, "nextOrderId()", block)
    if next_id > 10**9 or next_id < 1:
        raise RPCError("Implausible nextOrderId; verify deployed ABI")
    start = max(1, next_id - max_orders)
    gas_price = int(rpc.rpc("eth_gasPrice", []), 16)
    weth = address(rpc.uint(RANGE_ORDERS, "weth()", block)).lower()
    rows, errors, token_cache = [], [], {}
    for oid in range(start, next_id):
        try:
            item = decode_order(rpc.call(RANGE_ORDERS, calldata("orders(uint256)", oid), block))
            if item["status"] != "open":
                continue
            item.update({"order_id": oid, "block": block_number})
            item["fillable"] = bool(rpc.uint(RANGE_ORDERS, "fillable(uint256)", block, oid))
            item["status_label"] = "NOT_FILLABLE"
            if item["fillable"]:
                token_function = "token1()" if item["zero_for_one"] else "token0()"
                out_token = address(rpc.uint(item["pool"], token_function, block))
                if out_token not in token_cache:
                    token_cache[out_token] = token_info(rpc, out_token, block)
                tok = token_cache[out_token]
                bounty_raw = estimated_bounty_raw(item["liquidity"], item["tick_lower"],
                                                   item["tick_upper"], item["zero_for_one"])
                amount = Decimal(bounty_raw) / (Decimal(10) ** tok["decimals"])
                item.update({
                    "payout_token": tok["symbol"], "payout_address": out_token,
                    "indicative_bounty_tokens": str(amount),
                    "calculation_warning": "FULLY_CROSSED_PRINCIPAL_ESTIMATE_NOT_VERIFIED_PAYOUT"
                })
                gas = None
                if sim_from:
                    try:
                        gas = rpc.estimate_gas({
                            "from": sim_from, "to": RANGE_ORDERS,
                            "data": calldata("fill(uint256)", oid), "value": "0x0"
                        })
                        item["gas_simulation"] = "SUCCESS_GAS_ESTIMATE_ONLY"
                    except RPCError:
                        item["gas_simulation"] = "FAILED_OR_REVERTED"
                else:
                    item["gas_simulation"] = "NOT_ATTEMPTED_NO_PUBLIC_CALLER_ADDRESS"
                item["gas_units"] = gas
                item["screening_gas_ceiling"] = gas_ceiling
                gas_eth = Decimal(gas if gas is not None else gas_ceiling) * Decimal(gas_price) * gas_multiplier / Decimal(10**18)
                item["indicative_gas_cost_eth"] = str(gas_eth)
                token_price = eth_usd if out_token.lower() == weth else prices.get(out_token.lower())
                if token_price is not None and eth_usd is not None:
                    gross = amount * token_price
                    gas_usd = gas_eth * eth_usd
                    item["indicative_gross_usd"] = str(gross)
                    item["indicative_net_before_exits_usd"] = str(gross - gas_usd)
                    item["status_label"] = (
                        "SIMULATION_REQUIRED" if gas is None else
                        "BELOW_THRESHOLD" if gross - gas_usd <= min_profit_usd else
                        "WATCH_ONLY_NOT_EXECUTION_READY"
                    )
                else:
                    item["status_label"] = "PRICE_UNAVAILABLE"
            rows.append(item)
        except (ValueError, RPCError, ArithmeticError, OverflowError) as exc:
            errors.append({"order_id": oid, "error": str(exc)[:250]})
    return {
        "source": "read-only on-chain RPC", "chain_id": chain,
        "network": "Robinhood Chain", "contract": RANGE_ORDERS,
        "block_number": block_number, "next_order_id": next_id,
        "scan_window": [start, max(start, next_id - 1)],
        "scan_is_full_history": start == 1,
        "gas_price_gwei": str(Decimal(gas_price) / Decimal(10**9)),
        "orders_scanned": max(0, next_id - start),
        "open_orders": len(rows),
        "fillable_orders": sum(bool(x["fillable"]) for x in rows),
        "errors": errors, "orders": rows,
        "transactions_sent": 0, "funds_spent_usd": 0,
        "status": "WATCH_ONLY_NOT_EXECUTION_READY",
        "disclaimer": "All rewards indicative; prices manually supplied; no sale or priority costs included."
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rpc", default=os.environ.get("ROBINHOOD_RPC_URL", DEFAULT_RPC))
    p.add_argument("--max-orders", type=int, default=100)
    p.add_argument("--sim-from", help="Public EVM caller address, NEVER a key")
    p.add_argument("--eth-usd", type=Decimal, help="Independently verified USD price; no live oracle")
    p.add_argument("--prices", help="JSON mapping token addresses to user-verified USD prices")
    p.add_argument("--min-profit-usd", type=Decimal, default=Decimal("1"))
    p.add_argument("--gas-multiplier", type=Decimal, default=Decimal("1.5"))
    p.add_argument("--gas-ceiling", type=int, default=500000)
    p.add_argument("--output", default="report.json")
    a = p.parse_args(argv)
    if not 1 <= a.max_orders <= 2000:
        p.error("--max-orders must be between 1 and 2000")
    if a.sim_from and not HEX_ADDRESS.fullmatch(a.sim_from):
        p.error("--sim-from must be a PUBLIC 0x address")
    if a.eth_usd is not None and (not a.eth_usd.is_finite() or a.eth_usd <= 0):
        p.error("--eth-usd must be positive")
    if a.gas_multiplier < 1 or a.gas_ceiling < 21000:
        p.error("gas multiplier >= 1 and gas ceiling >= 21000 required")
    try:
        result = scan(JSONRPC(a.rpc), a.max_orders, a.sim_from,
                      read_prices(a.prices), a.eth_usd, a.gas_multiplier,
                      a.gas_ceiling, a.min_profit_usd)
    except (RPCError, ValueError, OSError) as exc:
        print(f"SCAN FAILED: {exc}; no opportunity inference.", file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    print(f"Block {result['block_number']}; open {result['open_orders']}; fillable {result['fillable_orders']}; errors {len(result['errors'])}")
    for order in result["orders"]:
        if order["fillable"]:
            print(f"#{order['order_id']} ~{order['indicative_bounty_tokens']} {order['payout_token']} | {order['status_label']}")
    print("READ ONLY. No transactions sent. Output:", a.output)
    return 3 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
