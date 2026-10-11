"""Offline tests for Base Superfluid receipt scanner (no RPC or wallet)."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import superfluid_receipts as s


def transfer(src, dst, raw):
    return {"address": s.ETHX, "topics": [
        s.TRANSFER, "0x" + src[2:].rjust(64, "0"),
        "0x" + dst[2:].rjust(64, "0")],
        "data": "0x" + f"{raw:064x}"}


class Tests(unittest.TestCase):
    def test_positive_transfer_and_fee(self):
        sender = "0x" + "4" * 40
        tx = {"hash": "0x" + "a" * 64, "from": sender}
        receipt = {
            "status": "0x1", "blockNumber": hex(45764677),
            "gasUsed": hex(629867), "effectiveGasPrice": hex(7200000),
            "l1Fee": hex(1962147885),
            "logs": [
                transfer("0x" + "1"*40, sender, 277410573088982),
                {"address": s.ETHX, "topics": [s.LIQUIDATION], "data": "0x"}
            ]
        }
        r = s.parse_receipt(tx, receipt)
        self.assertEqual(r["ethx_received_raw"], "277410573088982")
        self.assertEqual(r["liquidation_events"], 1)
        self.assertEqual(r["full_fee_wei"], str(629867*7200000+1962147885))

    def test_missing_l1_fee_is_not_estimated_as_full(self):
        sender = "0x" + "2" * 40
        r = s.parse_receipt(
            {"hash": "0x" + "a" * 64, "from": sender},
            {"status": "0x1", "blockNumber": "0x3", "gasUsed": "0x1",
             "effectiveGasPrice": "0x2", "logs": []})
        self.assertEqual(r["completeness"], "L1_FEE_MISSING")
        self.assertIsNone(r["full_fee_wei"])

    def test_failed_transaction(self):
        r = s.parse_receipt({"hash": "0x" + "a" * 64}, {"status": "0x0"})
        self.assertEqual(r["status"], "FAILED")

    def test_no_false_payout_to_other_address(self):
        sender = "0x" + "2" * 40
        r = s.parse_receipt(
            {"hash": "0x" + "a" * 64, "from": sender},
            {"status": "0x1", "blockNumber": "0x3", "gasUsed": "0x1",
             "effectiveGasPrice": "0x2",
             "logs": [transfer("0x" + "1"*40, "0x" + "3"*40, 999)]})
        self.assertEqual(r["ethx_received_raw"], "0")


if __name__ == "__main__":
    unittest.main()
