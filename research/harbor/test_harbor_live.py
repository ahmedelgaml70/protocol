import unittest
from unittest.mock import patch
import harbor_live as h
class HarborTests(unittest.TestCase):
  def test_selector_calldata_address(self):
    c=h.calldata("harvest(address,uint256)",h.DUMMY)
    self.assertEqual(len(c),10+64+64)
    self.assertEqual(c[10+24:10+64].lower(),h.DUMMY[2:].lower())
  def test_no_mutation_or_signing(self):
    for method in ["eth_sendTransaction","eth_sendRawTransaction","personal_sign","eth_sign"]:
      with self.subTest(method=method):
        with self.assertRaisesRegex(ValueError,"blocked"):h.rpc("rpc",method,[])
  def test_zero_harvest_bounty_never_simulated(self):
    signals={"decimals()":18,"harvestBountyRatio()":10**16,
        "harvestable()":0,"harvestCutRatio()":0,
        "rebalanceBountyRatio()":0,"rebalanceable()":0}
    def mocked(url,method,params=()):
      if method=="eth_chainId":return "0x1"
      if method=="eth_blockNumber":return "0x123"
      if method=="eth_gasPrice":return "0x3b9aca00"
      if method=="eth_getCode":return "0x6001"
      raise AssertionError("no estimate or mutate allowed: "+method)
    with patch.object(h,"rpc",side_effect=mocked),patch.object(h,"query",side_effect=lambda url,address,sig:signals[sig]):
      report=h.check("rpc")
    self.assertEqual(report["positive_harvest_bounty_markets"],0)
    self.assertEqual(report["rebalance_possible_markets"],0)
    self.assertEqual(report["observed_markets"],5)
    self.assertTrue(all(x["harvest_simulation"]=="not_attempted" for x in report["markets"]))
  def test_ethers_are_not_usd(self):
    self.assertNotIn("cashable_usd",h.MARKETS)
if __name__=="__main__":unittest.main()
