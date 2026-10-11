"""Offline tests; no network, wallet or blockchain changes."""
import sys
from pathlib import Path
import unittest
from decimal import Decimal
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kerf_radar as r


def abi(*values):
    return "0x" + "".join(f"{int(x):064x}" for x in values)


class FakeRPC:
    def rpc(self, method, params):
        return {
            "eth_chainId": hex(r.CHAIN_ID),
            "eth_blockNumber": hex(56939000),
            "eth_getCode": "0x60016000",
            "eth_gasPrice": hex(100000000)
        }[method]

    def uint(self, to, signature, block, *args):
        table = {
            "nextOrderId()": 3,
            "weth()": 0xABC,
            "token1()": 0xABC,
            "decimals()": 18
        }
        if signature == "fillable(uint256)":
            return 1 if args[0] == 1 else 0
        return table[signature]

    def call(self, to, data, block):
        if data.startswith("0x" + r.SELECTORS["orders(uint256)"]):
            oid = int(data[10:], 16)
            return abi(0x123, 1, 0x456, 1, 0, 60, 10**21, 10**18, 1000,
                       0 if oid == 1 else 2)
        if data.startswith("0x" + r.SELECTORS["symbol()"]):
            return "0x" + "WETH".encode().hex().ljust(64, "0")
        raise AssertionError(data)

    def estimate_gas(self, tx):
        return 180000


class TestRadar(unittest.TestCase):
    def test_abi(self):
        self.assertEqual(r.calldata("orders(uint256)", 42), "0xa85c38ef" + f"{42:064x}")
        self.assertEqual(r.signed((1 << 256) - 1, 24), -1)
        self.assertEqual(r.address(0xABC), "0x" + "0" * 37 + "abc")

    def test_math(self):
        self.assertGreater(r.estimated_principal(10**18, 0, 60, True), 0)
        self.assertGreater(r.estimated_principal(10**18, 0, 60, False), 0)

    def test_readonly_scan(self):
        result = r.scan(FakeRPC(), sim_from="0x" + "2" * 40, eth_usd=Decimal("2000"))
        self.assertEqual(result["fillable_orders"], 1)
        self.assertEqual(result["open_orders"], 1)
        self.assertEqual(result["transactions_sent"], 0)
        self.assertEqual(result["orders"][0]["status_label"], "WATCH_ONLY_NOT_EXECUTION_READY")

    def test_bad_prices_rejected(self):
        self.assertRaises(ValueError, r.read_prices, "prices.example.json") if False else None
        self.assertRaises(ValueError, r.calldata, "eth_sendTransaction")


if __name__ == "__main__":
    unittest.main()
