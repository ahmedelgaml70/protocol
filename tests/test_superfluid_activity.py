"""Offline validation of Superfluid subgraph summary (no network/wallet)."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from superfluid_activity import summarize


def sample(timestamp="1778318701", reward="131570295251418"):
    return {"timestamp": timestamp, "transactionHash": "0x"+"1"*64,
        "token": "0x"+"a"*40, "liquidatorAccount": "0x"+"f"*40,
        "rewardAmountReceiver": "0x"+"f"*40, "rewardAmount": reward, "liquidationType": 1}


class TestActivity(unittest.TestCase):
    def test_one_successful_indexed_event(self):
        result = summarize([sample()], 1778310000, 1778320000, 10)
        self.assertEqual(result["events_sampled"], 1)
        self.assertEqual(result["unique_indexed_liquidator_addresses"], 1)
        self.assertFalse(result["sample_may_be_truncated"])
        self.assertFalse(result["profit_usd_verified"])

    def test_saturated_sample_is_flagged(self):
        self.assertTrue(summarize([sample()], 1778310000, 1778320000, 1)["sample_may_be_truncated"])

    def test_out_of_window_rejected(self):
        with self.assertRaises(ValueError):
            summarize([sample(timestamp="10")], 1000, 2000, 10)


if __name__ == "__main__":
    unittest.main()
