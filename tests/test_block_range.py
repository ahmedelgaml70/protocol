"""Offline tests for wall-clock historical scan window."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from block_range import start_block_for_hours


class FakeRPC:
    def rpc(self, method, params):
        assert method == "eth_getBlockByNumber"
        block_num = int(params[0], 16)
        return {"timestamp": hex(1_000_000 + block_num * 10)}


class TestRange(unittest.TestCase):
    def test_exact_hour_cutoff(self):
        self.assertEqual(start_block_for_hours(FakeRPC(), 1000, 0, 1), 640)

    def test_deployment_boundary(self):
        self.assertEqual(start_block_for_hours(FakeRPC(), 1000, 500, 24), 500)

    def test_reject_invalid_parameters(self):
        with self.assertRaises(ValueError):
            start_block_for_hours(FakeRPC(), 10, 11, 1)
        with self.assertRaises(ValueError):
            start_block_for_hours(FakeRPC(), 100, 0, 0)


if __name__ == "__main__":
    unittest.main()
