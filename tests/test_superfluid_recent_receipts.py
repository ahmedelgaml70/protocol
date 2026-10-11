"""Offline receipt sampling tests; no wallet and no external requests."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from superfluid_recent_receipts import select_transactions, audit_receipts, BATCH_LIQUIDATOR, ETHX
from superfluid_receipts import TRANSFER


def event(no, when, raw):
    return {"token_address": ETHX, "transaction_hash": "0x" + f"{no:064x}",
            "timestamp_utc": when, "reward_raw": str(raw), "liquidation_type_code": 1}


class FakeRPC:
    def rpc(self, method, params):
        if method == "eth_chainId":
            return hex(8453)
        tx_hash = params[0]
        if method == "eth_getTransactionByHash":
            return {"hash": tx_hash, "from": "0x" + "2"*40}
        if method == "eth_getTransactionReceipt":
            return {
                "status": "0x1", "blockNumber": "0x1",
                "gasUsed": "0x64", "effectiveGasPrice": "0x2", "l1Fee": "0x5",
                "logs": [{"address": ETHX, "topics": [
                    TRANSFER, "0x" + BATCH_LIQUIDATOR[2:].rjust(64, "0"),
                    "0x" + ("2"*40).rjust(64, "0")],
                    "data": "0x" + f"{2000000000000000:064x}"}]
            }
        raise AssertionError("Unapproved RPC method")


class TestReceiptSampler(unittest.TestCase):
    def test_dedup_and_largest(self):
        data={"network":"base-mainnet","events":[
            event(1,"2026-10-08T00:00:01Z",10),
            event(1,"2026-10-08T00:00:01Z",20),
            event(2,"2026-10-11T00:00:01Z",1)]}
        selected, n=select_transactions(data,2)
        self.assertEqual(n,2)
        self.assertEqual(selected[0][1]["reward_raw"],30)

    def test_fee_and_receipt(self):
        data={"network":"base-mainnet","events":[event(1,"2026-10-11T00:00:01Z",100)]}
        out=audit_receipts(data,FakeRPC(),1)
        self.assertEqual(out["rows"][0]["reported_full_gas_fee_wei"],"205")
        self.assertEqual(out["rows"][0]["ethx_to_eth_parity_proxy_after_gas"],
                         "0.001999999999999795")
        self.assertEqual(out["transactions_sent"],0)
        self.assertIsNone(out["verified_realized_profit_usd"])

    def test_other_network_rejected(self):
        with self.assertRaises(ValueError):
            select_transactions({"network":"polygon-mainnet","events":[]},1)


if __name__ == "__main__":
    unittest.main()
