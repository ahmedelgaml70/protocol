"""Offline unit tests for Kerf's additional historical bounty observer."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kerf_multi_history as m


def abi(*vals):
    return "0x" + "".join(f"{v:064x}" for v in vals)


def event(topic, address, topics=None, words=()):
    return {
        "address": address, "topics": [topic] + (topics or []),
        "data": abi(*words), "blockNumber": hex(800),
        "transactionHash": "0x" + "a" * 64
    }


TOP_VAULT = "0xd7612277cfab99e98a6e102dadbfb19c48b33e6bd1ba17ee3b1778c2c04ef888"
TOP_KEEPER = "0x68cf8717f566d6a94c69f0a80648ec78112c770669f3f1c33183693e7e9c8c48"
TOP_PERP = "0xf4c6cbfcc96248be8ecbaf76de0fee34f71f2fadd9af537dd38c2657621930d6"


class TestBounties(unittest.TestCase):
    def test_vault_harvest(self):
        msg = event(TOP_VAULT, m.SEED_VAULTS["ETH Vault"],
                    words=(100, 200, 10, 20, 1, 2))
        decoded = m.decode_event(msg)
        self.assertEqual(decoded["kind"], "VaultHarvest")
        self.assertEqual(decoded["bounty1_raw"], "2")
        self.assertEqual(decoded["vault"], "ETH Vault")

    def test_position_harvest(self):
        msg = event(TOP_KEEPER, m.KEEPER, [hex(7), hex(0x123)],
                    words=(100, 1000, 2, 3, 1))
        parsed = m.decode_event(msg)
        self.assertEqual(parsed["token_id"], 7)
        self.assertEqual(parsed["bounty0_raw"], "2")
        self.assertTrue(parsed["compounded"])

    def test_perp_liquidation(self):
        msg = event(TOP_PERP, m.PERP, [hex(8), hex(0x777)], words=(500,))
        parsed = m.decode_event(msg)
        self.assertEqual(parsed["position_id"], 8)
        self.assertEqual(parsed["bounty_usdg_raw"], "500")

    def test_unknown_topics_ignored(self):
        msg = event("0x" + "0" * 64, m.PERP, words=(0,))
        self.assertIsNone(m.decode_event(msg))

    def test_event_accounting(self):
        a = m.decode_event(event(TOP_VAULT, m.SEED_VAULTS["ETH Vault"],
                                 words=(100, 200, 10, 20, 1, 2)))
        b = m.decode_event(event(TOP_KEEPER, m.KEEPER, [hex(7), hex(0x123)],
                                 words=(100, 1000, 0, 0, 0)))
        c = m.decode_event(event(TOP_PERP, m.PERP, [hex(8), hex(0x777)], words=(500,)))
        summary = m.summarize([a, b, c], 1, 1000)
        self.assertEqual(summary["positive_reward_event_counts"]["vault_positive_bounties"], 1)
        self.assertEqual(summary["positive_reward_event_counts"]["position_positive_bounties"], 0)
        self.assertEqual(summary["positive_reward_event_counts"]["perp_positive_bounties"], 1)
        self.assertEqual(summary["unique_position_keeper_callers"], 1)
        self.assertEqual(summary["transactions_sent"], 0)

    def test_malformed_event_fails_closed(self):
        msg = event(TOP_PERP, m.PERP, [hex(8), hex(0x777)], words=())
        with self.assertRaises(ValueError):
            m.decode_event(msg)


if __name__ == "__main__":
    unittest.main()
