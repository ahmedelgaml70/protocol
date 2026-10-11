"""Synthetic historical event parse test; no live blockchain dependency."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kerf_history as h


class FakeRPC:
    def rpc(self, method, params):
        if method != "eth_getLogs":
            raise AssertionError(method)
        log = {
            "topics": [
                "0xdef4cdb91e8c5e2777b0bf9645ce2c7e0b64a3b3fb94e37c6d78cde1043f80cb",
                hex(12), hex(0xABC)
            ],
            "data": "0x" + "".join(f"{x:064x}" for x in (100, 3, 1)),
            "blockNumber": hex(50), "transactionHash": "0x" + "a" * 64
        }
        return [log]


class TestHistory(unittest.TestCase):
    def test_filled_event_and_summary(self):
        events = h.fetch_events(FakeRPC(), 50, 51, 2)
        self.assertEqual(events[0]["bounty_raw"], "1")
        self.assertEqual(events[0]["order_id"], 12)
        result = h.summarize(events, 4663, 50, 51)
        self.assertEqual(result["filled_events"], 1)
        self.assertEqual(result["unique_keeper_addresses"], 1)
        self.assertEqual(result["transactions_sent"], 0)


if __name__ == "__main__":
    unittest.main()
