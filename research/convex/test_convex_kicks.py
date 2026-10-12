import unittest
from unittest.mock import patch
from eth_abi import encode
import convex_kicks as k

class KickTests(unittest.TestCase):
    def test_exact_topics(self):
        self.assertEqual(len(k.KICK),66)
        self.assertEqual(k.LOCKER.lower(),"0x72a19342e8f1838460ebfccef09f6585e32db86e")
    def test_wrong_chain_rejected(self):
        with patch.object(k.b,"rpc",return_value="0x89"):
            with self.assertRaisesRegex(RuntimeError,"Wrong chain"):
                k.audit("rpc")
    def test_mock_paid_kick(self):
        recipient="0x"+"11"*20
        user="0x"+"22"*20
        ev={"topics":[k.KICK,"0x"+"00"*12+recipient[2:],
                      "0x"+"00"*12+user[2:]],"data":"0x"+encode(["uint256"],[100*10**18]).hex(),
            "transactionHash":"0x"+"33"*32,"blockNumber":"0x01"}
        def mocked(url,method,params=()):
            if method=="eth_chainId":return "0x1"
            if method=="eth_getCode":return "0x6001"
            if method=="eth_blockNumber":return "0x64"
            if method=="eth_getLogs":return [ev] if int(params[0]["fromBlock"],16)==0 else []
            if method=="eth_getTransactionByHash":return {"from":recipient}
            if method=="eth_getTransactionReceipt":return {"status":"0x1","gasUsed":"0x5208","effectiveGasPrice":"0x3b9aca00"}
            raise AssertionError(method)
        with patch.object(k.b,"rpc",side_effect=mocked),patch.object(k,"read_param",return_value=100):
            r=k.audit("rpc")
        self.assertEqual(r["total_historical_kick_cvx"],"100")
        self.assertEqual(r["kick_events"],1)
    def test_no_signing_methods_inherited(self):
        with self.assertRaisesRegex(ValueError,"blocked"):
            k.b.rpc("rpc","eth_sendTransaction",[])
if __name__=="__main__":unittest.main()
