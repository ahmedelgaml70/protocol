"""Synthetic indexed events; no API or wallet access."""
import unittest
from datetime import datetime, timezone
from morpho_liquidations import summarize

NOW=datetime(2026,10,12,6,0,tzinfo=timezone.utc)
def evt(day=12,raw="123",tx="a",who="2"):
    return {
      "type":"Liquidation","timestamp":str(int(datetime(2026,10,day,5,0,tzinfo=timezone.utc).timestamp())),
      "txHash":"0x"+tx*64,"blockNumber":"52499000",
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
    def test_bad_hash_refused(self):
        r=evt();r["txHash"]="bad"
        with self.assertRaises(ValueError):summarize([r],NOW,7,100)
    def test_unequal_asset_decimals_not_priced(self):
        o=summarize([evt(raw="1000000")],NOW,7,100)
        self.assertNotIn("profit_usd",o["events"][0])
if __name__=="__main__":
    unittest.main()
