"""Offline tests for time-accurate block ranges and pruned-history RPCs."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from block_range import start_block_for_hours


class FakeRPC:
    def __init__(self, pruned_before=0):
        self.pruned_before = pruned_before
        self.seen = []

    def rpc(self, method, params):
        assert method == "eth_getBlockByNumber"
        block_num = int(params[0], 16)
        self.seen.append(block_num)
        if block_num < self.pruned_before:
            raise ValueError("PRUNED_HISTORY")
        return {"timestamp": hex(1_000_000 + block_num * 10)}


class TestRange(unittest.TestCase):
    def test_exact_hour_cutoff(self):
        self.assertEqual(start_block_for_hours(FakeRPC(), 1000, 0, 1), 640)

    def test_deployment_boundary(self):
        self.assertEqual(start_block_for_hours(FakeRPC(), 1000, 500, 24), 500)

    def test_pruned_genesis_not_queried(self):
        provider = FakeRPC(pruned_before=99_000)
        self.assertEqual(start_block_for_hours(provider, 100_000, 1, 1), 99_640)
        self.assertGreaterEqual(min(provider.seen), 99_000)

    def test_near_tip(self):
        self.assertEqual(start_block_for_hours(FakeRPC(), 100_000, 1, 0.01), 99_997)

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            start_block_for_hours(FakeRPC(), 10, 11, 1)
        with self.assertRaises(ValueError):
            start_block_for_hours(FakeRPC(), 100, 0, 0)


if __name__ == "__main__":
    unittest.main()
