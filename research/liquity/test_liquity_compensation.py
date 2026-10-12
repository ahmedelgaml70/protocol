import unittest
from unittest.mock import patch
from eth_abi import encode
import liquity_compensation as p

class LiquityTests(unittest.TestCase):
    def test_v1_event_decoding(self):
        vals=[1200*10**18,3*10**18,10**16,200*10**18]
        event={"data":"0x"+encode(["uint256"]*4,vals).hex(),
               "transactionHash":"0x"+"22"*32,"blockNumber":"0x20"}
        item=p.event_info("v1_eth",event)
        self.assertEqual(item["fee_token_units"],"200")
        self.assertEqual(item["collateral_compensation_token_units"],"0.01")
    def test_v2_event_decoding(self):
        vals=[1,2,375*10**14,5*10**16,5,6,7,8,9,10]
        event={"data":"0x"+encode(["uint256"]*10,vals).hex(),
               "transactionHash":"0x"+"33"*32,"blockNumber":"0x20"}
        item=p.event_info("v2_eth",event)
        self.assertEqual(item["fee_token_units"],"0.0375")
        self.assertEqual(item["collateral_compensation_token_units"],"0.05")
    def test_reject_non_exact_event(self):
        event={"data":"0x00","transactionHash":"0x","blockNumber":"0x2"}
        with self.assertRaisesRegex(ValueError,"length mismatch"):
            p.event_info("v2_eth",event)
    def test_rpc_rejects_signing_and_sending(self):
        for method in ["eth_sendTransaction","eth_sendRawTransaction",
                       "personal_sign","eth_sign","eth_signTypedData_v4"]:
            with self.subTest(method=method):
                with self.assertRaisesRegex(ValueError,"blocked"):
                    p.rpc("https://example.invalid",method,[])
    def test_partial_logs_are_incomplete(self):
        def fake_rpc(url,method,params=()):
            if method=="eth_getCode":return "0x6001"
            if method=="eth_getLogs":raise RuntimeError("blocked")
            raise AssertionError(method)
        with patch.object(p,"rpc",side_effect=fake_rpc):
            r=p.historical("rpc",8000)
        self.assertEqual(r["successful_branches"],0)
        self.assertEqual(r["incomplete_branches"],4)
        self.assertTrue(all(x["status"]=="incomplete" for x in r["branches"]))
    def test_transfer_recipient_logic(self):
        direct_topic="0x"+"0"*24+"22"*20
        sender="0x"+"22"*20
        row={"transaction_hash":"0x"+"33"*32,"fee_token":p.WETH}
        tx={"from":sender,"to":p.SCOPE["v2_eth"]["manager"]}
        transfer={"address":p.WETH,"topics":[p.TRANSFER_TOPIC,
           "0x"+"0"*24+"44"*20,direct_topic],
           "data":hex(375*10**14)}
        receipt={"status":"0x1","gasUsed":"0x5208",
                 "effectiveGasPrice":"0x3b9aca00","logs":[transfer]}
        with patch.object(p,"rpc",side_effect=lambda url,method,params:
                          tx if method=="eth_getTransactionByHash" else receipt):
            p.receipt_check("rpc",row)
        self.assertEqual(row["receipt"]["direct_fee_token_to_sender_units"],"0.0375")

if __name__=="__main__":unittest.main()
