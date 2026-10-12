import unittest
from unittest.mock import patch
import live as p
class MotoTests(unittest.TestCase):
 def test_no_money_methods(self):
  for name in ("eth_sendTransaction","eth_sendRawTransaction","eth_sign","personal_sign","eth_sendUserOperation"):
   with self.assertRaisesRegex(ValueError,"blocked"):p.rpc("invalid",name,[])
  for name in ("/motofun/coins/abc","/backend-fun/mainnet/intents","/motofun/private"):
   with self.assertRaisesRegex(ValueError,"allowlisted"):p.get_json(name)
 def test_selector_and_address_encoding(self):
  s=p.word_address("graduate(address)",p.DUMMY)
  self.assertEqual(len(s),74)
  self.assertEqual(s[10:],("0"*24)+("1"*40))
 def test_bad_chain(self):
  with patch.object(p,"rpc",return_value="0x89"):
   with self.assertRaisesRegex(ValueError,"wrong Ethereum"):p.inspect({"motofunEnabled":True}, {}, [],"rpc")
 def test_disabled_not_fundable(self):
  with patch.object(p,"rpc",return_value="0x1"):
   v=p.inspect({"motofunEnabled":False,"addresses":{"launchpadCurve":p.ZERO,"launchpadLens":p.DUMMY}}, {}, [],"rpc")
   self.assertEqual(v["status"],"official_api_reports_disabled")
if __name__=="__main__":unittest.main()
