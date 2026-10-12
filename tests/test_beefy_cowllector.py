"""Cowllector reports are estimates and must never be promoted as opportunities."""
import unittest
from datetime import datetime, timedelta, timezone
from beefy_cowllector import summarize

NOW=datetime(2026,10,12,5,0,tzinfo=timezone.utc)

def row(**kwargs):
    item={
        "chain":"base",
        "datetime": (NOW-timedelta(hours=1)).isoformat(),
        "eol":False, "run_ok":True,
        "vault_id":"base-vault", "strategy_address":"0x"+"a"*40,
        "simulation_ok":True,
        "simulation_gas_estimated_call_rewards_wei":500,
        "simulation_gas_transaction_cost_estimation_wei":300,
        "simulation_gas_estimated_gain_wei":200,
        "summary_harvested":True, "transaction_ok":True,
        "transaction_hash":"0x"+"b"*64
    }
    item.update(kwargs)
    return item

class BeefyTests(unittest.TestCase):
    def test_positive_operator_estimate_not_realized_profit(self):
        o=summarize([row()],NOW)
        self.assertEqual(o["estimated_positive_margin_rows"],1)
        self.assertFalse(o["profit_usd_verified"])
        self.assertFalse(o["top_estimated_positive_margin_reports"][0]["currently_available"])
        self.assertFalse(o["top_estimated_positive_margin_reports"][0]["actual_caller_payout_verified"])

    def test_negative_estimate_rejected(self):
        o=summarize([row(simulation_gas_estimated_call_rewards_wei=200)],NOW)
        self.assertEqual(o["estimated_positive_margin_rows"],0)

    def test_stale_and_eol_excluded(self):
        o=summarize([row(datetime=(NOW-timedelta(days=7)).isoformat()),
                     row(eol=True)],NOW)
        self.assertEqual(o["estimated_positive_margin_rows"],0)


    def test_missing_simulation_distinct_from_loss(self):
        o=summarize([row(simulation_ok=False),row(simulation_gas_estimated_call_rewards_wei=None)],NOW)
        stages=o["evidence_funnel"]
        self.assertEqual(stages.get("simulation_not_ok"),1)
        self.assertEqual(stages.get("simulation_reward_or_gas_missing"),1)
        self.assertEqual(stages.get("simulated_nonpositive_margin",0),0)

    def test_bad_chain_rejected(self):
        with self.assertRaises(ValueError):
            summarize([],NOW,chains=["ethereum-classic"])

    def test_unsupported_schema_does_not_fabricate_rewards(self):
        o=summarize([{"chain":"base","datetime":NOW.isoformat(),"eol":False}],NOW)
        self.assertEqual(o["estimated_positive_margin_rows"],0)

if __name__=="__main__":
    unittest.main()
