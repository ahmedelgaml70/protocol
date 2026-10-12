import unittest
from unittest.mock import patch
from eth_abi import encode
from eth_utils import keccak
import splits_expanded as p

SAMPLE=(["0x"+"11"*20,"0x"+"22"*20],[40,60],100,10000)

class ExpandedTests(unittest.TestCase):
    def test_factory_and_chain_coverage(self):
        self.assertEqual(set(p.FACTORIES),{"v2","v2o1","v2o2"})
        self.assertEqual(set(p.CHAINS),{"base","optimism","arbitrum"})
        self.assertEqual(len(p.CREATED),3)

    def test_created_event_dynamic_tuple_with_remaining_fields(self):
        data=encode([p.SPLIT,"address","address"],
                    [SAMPLE,"0x"+"33"*20,"0x"+"44"*20])
        event={"topics":[p.CREATED[0],"0x"+"00"*12+"55"*20],
               "data":"0x"+data.hex()}
        address, params=p.parse_created(event)
        self.assertEqual(address.lower(),"0x"+"55"*20)
        self.assertEqual(params[3],10000)

    def test_creation_hash_matches_live(self):
        hashed=keccak(encode([p.SPLIT],[SAMPLE]))
        with patch.object(p.base,"call",return_value=hashed):
            with patch.object(p.base,"events",side_effect=AssertionError("unexpected logs")):
                config,proof=p.verified_config("url","0x"+"44"*20,SAMPLE,100)
        self.assertEqual(config[3],10000)
        self.assertIn("matches",proof)

    def test_stale_event_is_rejected(self):
        with patch.object(p.base,"call",return_value=b"not matching"):
            with patch.object(p.base,"events",return_value=[]):
                with self.assertRaisesRegex(ValueError,"Changed configuration"):
                    p.verified_config("url","0x"+"44"*20,SAMPLE,10000)

    def test_actual_timestamps_binary_search(self):
        def mock_rpc(url,method,args):
            self.assertEqual(method,"eth_getBlockByNumber")
            n=int(args[0],16)
            return {"timestamp":hex(1000+n*2)}
        with patch.object(p.base,"rpc",side_effect=mock_rpc):
            self.assertEqual(p.timestamp_block("url",100,1099),49)

    def test_wrong_chain_is_incomplete_not_empty(self):
        with patch.object(p.base,"rpc",return_value=hex(123)):
            with self.assertRaisesRegex(RuntimeError,"Chain ID mismatch"):
                p.scan("url","base")

    def test_only_read_only_methods_allowed(self):
        with self.assertRaisesRegex(ValueError,"blocked"):
            p.base.rpc("unused","eth_sendRawTransaction",[])

if __name__=="__main__":
    unittest.main()
