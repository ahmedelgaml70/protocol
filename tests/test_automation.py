"""No network or real GitHub token is used in these tests."""
from decimal import Decimal
import unittest
from scripts.assess_radar import evaluate

MANIFEST = {"schema_version": 1, "purpose": "READ_ONLY_RESEARCH",
            "checks": [{"scanner": "pooltogether-base", "status": "ok",
                        "report_file": "pooltogether_claim_history.json"}]}

def example():
    return {
        "chain_id": 8453,
        "prize_pool": "0x45b2010d8a4f08b53c9fa7544c51dfd9733732cb",
        "current_published_claimer": "0xcdCE635b774DE77cdF791647601dba64a75547ba",
        "prize_token_contract_verified_onchain": "0x" + "a" * 40,
        "receipt_samples": [{
            "transaction_hash": "0x" + "b" * 64,
            "transaction_destination": "0xcdCE635b774DE77cdF791647601dba64a75547ba",
            "sent_to_published_current_claimer": True,
            "event_claim_reward_tokens": "0.2",
            "reward_recipients": ["0x" + "1" * 40],
            "fee_recipient_is_submitter": True,
            "network_fee_wei": "123456",
            "l1_fee_available": True,
        }]
    }

class AutomationTests(unittest.TestCase):
    def test_current_eligible_historical_receipt_only(self):
        result = evaluate(MANIFEST, {"pooltogether-base": example()})
        self.assertEqual(len(result["signals"]), 1)
        self.assertFalse(result["execution_ready"])
        self.assertEqual(result["signals"][0]["status"], "RESEARCH_ONLY_NOT_EXECUTION_READY")

    def test_not_current_claimer_no_alert(self):
        r = example()
        r["receipt_samples"][0]["sent_to_published_current_claimer"] = False
        self.assertFalse(evaluate(MANIFEST, {"pooltogether-base": r})["signals"])

    def test_no_reward_no_alert(self):
        r = example()
        r["receipt_samples"][0]["event_claim_reward_tokens"] = "0"
        self.assertFalse(evaluate(MANIFEST, {"pooltogether-base": r})["signals"])

    def test_failed_scan_no_alert(self):
        m = dict(MANIFEST)
        m["checks"] = [{**MANIFEST["checks"][0], "status": "incomplete"}]
        self.assertFalse(evaluate(m, {"pooltogether-base": example()})["signals"])

    def test_superfluid_historical_events_not_trading_signal(self):
        result = evaluate(MANIFEST, {"superfluid-base": {"events_sampled": 400}})
        self.assertEqual(result["signals"], [])

if __name__ == "__main__":
    unittest.main()
