import unittest
from unittest.mock import patch
from eth_abi import decode,encode
import sovryn_zero as p
import liquity_compensation as base

class SovrynSafetyTests(unittest.TestCase):
    def test_verified_source_addresses(self):
        self.assertEqual(p.ZUSD.lower(),"0xdb107fa69e33f05180a4c2ce9c2e7cb481645c2d")
        self.assertEqual(len(p.TM),42)
        self.assertEqual(p.EVENT,"Liquidation(uint256,uint256,uint256,uint256)")
    def test_20_zusd_event_decoding(self):
        base.SCOPE["sovryn_zero"]={"manager":p.TM,"fee_token":p.ZUSD,
            "event":p.EVENT,"field_count":4}
        ev={"data":"0x"+encode(["uint256"]*4,[1,2,3,20*10**18]).hex(),
            "transactionHash":"0x"+"bb"*32,"blockNumber":"0x55"}
        item=base.event_info("sovryn_zero",ev)
        self.assertEqual(item["fee_token_units"],"20")
    def test_wrong_chain_rejected(self):
        with patch.object(base,"rpc",return_value="0x1"):
            with self.assertRaisesRegex(RuntimeError,"Wrong Rootstock"):
                p.audit("rpc")
    def test_no_money_methods(self):
        for method in ("eth_sendTransaction","eth_sendRawTransaction","personal_sign"):
            with self.assertRaises(ValueError):base.rpc("unused",method,[])

if __name__=="__main__":unittest.main()
