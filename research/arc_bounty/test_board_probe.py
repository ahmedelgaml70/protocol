import unittest
from unittest.mock import patch
import board_probe as b

class BoardProbeTests(unittest.TestCase):
    def test_external_and_mutating_endpoints_rejected(self):
        for site,path in [("https://evil.invalid","/api/v1/stats"),
                          ("https://arcbounty.app","/api/v1/bounties/1"),
                          ("https://arcbounty.app","/api/v1/claim")]:
            with self.assertRaisesRegex(ValueError,"blocked"):
                b.safe_get(site,path)
    def test_mainnet_and_funded_open_filter(self):
        data={"chainId":5042,"testnet":False,"count":3,"bounties":[
            {"status":"open","jobId":1,"rewardUsdc":"50",
             "workerPayoutUsdc":"49.50","reservedFor":None,"audience":"anyone"},
            {"status":"open","jobId":2,"rewardUsdc":"200",
             "workerPayoutUsdc":"198","reservedFor":"0x"+"1"*40,"audience":"anyone"},
            {"status":"paid","jobId":3,"rewardUsdc":"1000","workerPayoutUsdc":"990"}]}
        r=b.parse_open(b.NETWORKS["arc"],data)
        self.assertEqual(r["open_count"],2)
        self.assertEqual(r["unreserved_count"],1)
        self.assertEqual(r["unreserved_25plus_count"],1)
        self.assertEqual(r["unreserved_worker_net_usdc_before_gas_total"],"49.50")
    def test_testnet_rejected(self):
        data={"chainId":5042,"testnet":True,"bounties":[{"status":"open"}]}
        self.assertEqual(b.parse_open(b.NETWORKS["arc"],data)["status"],"incomplete_wrong_network")
    def test_untrusted_nan_not_funding(self):
        self.assertIsNone(b.decimal_or_none("NaN"))
        self.assertIsNone(b.decimal_or_none("-10"))
        self.assertEqual(str(b.decimal_or_none("0.10")),"0.10")

if __name__=="__main__":unittest.main()
