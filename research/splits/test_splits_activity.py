import unittest
from unittest.mock import patch
import splits_activity as p

class ActivityTests(unittest.TestCase):
    def test_decodes_indexed_distribution(self):
        log={"topics":[p.DISTRIBUTED,"0x"+"00"*12+"aa"*20,
                       "0x"+"00"*12+"bb"*20],
             "address":"0x"+"cc"*20,
             "data":hex(12345),"transactionHash":"0x"+"dd"*32,
             "blockNumber":"0x10"}
        row=p.decode_event(log)
        self.assertEqual(row["distributed_amount_raw"],"12345")
        self.assertEqual(row["token"].lower(),"0x"+"aa"*20)
        self.assertEqual(row["distributor"].lower(),"0x"+"bb"*20)

    def test_bounded_event_log_reads_without_address(self):
        with patch.object(p.rpcbase,"rpc",return_value=[]) as fake:
            self.assertEqual(p.fetch_logs("rpc",5,6),[])
        params=fake.call_args[0][2][0]
        self.assertEqual(params["topics"],[p.DISTRIBUTED])
        self.assertNotIn("address",params)

    def test_factory_unknown_rejected(self):
        from eth_abi import encode
        with patch.object(p.rpcbase,"call",return_value=encode(["address"],["0x"+"01"*20])):
            with self.assertRaisesRegex(ValueError,"known"):
                p.verify_emitter("rpc","0x"+"ff"*20)

    def test_no_transaction_broadcast(self):
        with self.assertRaisesRegex(ValueError,"blocked"):
            p.rpcbase.rpc("rpc","eth_sendTransaction",[{}])

if __name__=="__main__":
    unittest.main()
