"""Synthetic indexed events; no API or wallet access."""
import unittest
from datetime import datetime, timezone
from morpho_liquidations import summarize

NOW=datetime(2026,10,12,6,0,tzinfo=timezone.utc)
def evt(day=12,raw="123",tx="a",who="2"):
    return {
      "type":"Liquidation","timestamp":str(int(datetime(2026,10,day,5,0,tzinfo=timezone.utc).timestamp())),
      "txHash":"0x"+tx*64,"blockNumber":"52499000","logIndex":0,
      "market":{"marketId":"0x"+"b"*64},
      "data":{"repaidAssets":raw,"seizedAssets":"789","badDebtAssets":"0",
              "liquidator":"0x"+who*40}
    }
class Tests(unittest.TestCase):
    def test_recent_event_not_profit(self):
        o=summarize([evt()],NOW,7,100)
        self.assertEqual(o["recent_liquidation_records"],1)
        self.assertFalse(o["profit_usd_verified"])
        self.assertFalse(o["events"][0]["receipt_verified"])
    def test_stale_event_filtered(self):
        self.assertEqual(summarize([evt(day=1)],NOW,7,100)["recent_liquidation_records"],0)
    def test_saturated_sample_warned(self):
        self.assertTrue(summarize([evt()],NOW,7,1)["query_may_be_truncated"])
    def test_batched_events_in_same_tx_are_distinct(self):
        a=evt()
        b=evt()
        b["logIndex"]=1
        o=summarize([a,b],NOW,7,100)
        self.assertEqual(o["recent_liquidation_records"],2)
        self.assertEqual(o["unique_transaction_hashes"],1)
        self.assertEqual(o["top_indexed_liquidator_event_count"][0][1],2)

    def test_identical_log_event_deduplicated(self):
        a=evt()
        o=summarize([a,a],NOW,7,100)
        self.assertEqual(o["recent_liquidation_records"],1)
        self.assertEqual(o["top_indexed_liquidator_event_count"][0][1],1)

    def test_bad_hash_refused(self):
        r=evt();r["txHash"]="bad"
        with self.assertRaises(ValueError):summarize([r],NOW,7,100)
    def test_reference_spread_never_realized_profit(self):
        e=evt(raw="1000000")
        e["data"]["seizedAssets"]="600000000000000"
        e["market"]["loanAsset"]={"address":"0x"+"c"*40,"symbol":"USDC","decimals":6,"priceUsd":1}
        e["market"]["collateralAsset"]={"address":"0x"+"d"*40,"symbol":"WETH","decimals":18,"priceUsd":2000}
        result=summarize([e],NOW,7,100)
        proxy=result["events"][0]["indicative_current_reference_valuation"]
        self.assertEqual(float(proxy["gross_current_reference_spread_usd"]),0.2)
        self.assertFalse(proxy["is_historical_realized_profit"])
        self.assertEqual(result["current_reference_valued_event_count"],1)

    def test_missing_reference_price_is_unknown_not_zero(self):
        e=evt()
        e["market"]["loanAsset"]={"address":"0x"+"c"*40,"symbol":"TOKEN","decimals":18,"priceUsd":None}
        result=summarize([e],NOW,7,100)
        self.assertIsNone(result["events"][0]["indicative_current_reference_valuation"])
        self.assertEqual(result["current_reference_valued_event_count"],0)

    def test_unequal_asset_decimals_not_priced(self):
        o=summarize([evt(raw="1000000")],NOW,7,100)
        self.assertNotIn("profit_usd",o["events"][0])
if __name__=="__main__":
    unittest.main()
