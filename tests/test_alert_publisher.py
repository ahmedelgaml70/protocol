"""Read-only tests for issue text generation, no GitHub token or network."""
import unittest
from scripts.publish_alerts import build_managed_section, KEY

def sample():
    return {
        "key": KEY, "status": "RESEARCH_ONLY_NOT_EXECUTION_READY",
        "prize_token_address": "0x"+"a"*40,
        "claimer": "0xcdce635b774de77cdf791647601dba64a75547ba",
        "current_claims_observed": 1,
        "examples": [{"transaction_hash":"0x"+"b"*64, "accrued_reward_tokens":"0.2"}]
    }

class Tests(unittest.TestCase):
    def test_research_text_and_fingerprint(self):
        section, digest = build_managed_section(sample())
        self.assertIn("research only", section)
        self.assertIn("NOT a currently available bounty", section)
        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, build_managed_section(sample())[1])

    def test_reject_bad_hash(self):
        p=sample()
        p["examples"][0]["transaction_hash"]="evil"
        with self.assertRaises(ValueError): build_managed_section(p)

    def test_reject_execution_instruction(self):
        p=sample()
        p["status"]="EXECUTE_NOW"
        with self.assertRaises(ValueError): build_managed_section(p)

if __name__=="__main__":
    unittest.main()
