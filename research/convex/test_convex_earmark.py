import unittest
from unittest.mock import patch
from eth_abi import encode
import convex_earmark as c

class ConvexTests(unittest.TestCase):
    def test_selector_matches_source(self):
        self.assertEqual(len(c.EARMARK),10)
        self.assertEqual(c.sel("transfer(address,uint256)"),"0xa9059cbb")
    def test_no_send_or_sign(self):
        for method in ("eth_sendTransaction","eth_sendRawTransaction",
                       "personal_sign","eth_sign","eth_sendUserOperation"):
            with self.subTest(method=method):
                with self.assertRaisesRegex(ValueError,"blocked"):
                    c.rpc("invalid://",method,[])
    def test_wrong_chain_rejected(self):
        with patch.object(c,"rpc",return_value="0xa"):
            with self.assertRaisesRegex(RuntimeError,"Ethereum mainnet"):
                c.inspect("rpc")
    def test_real_transfer_recipient_must_be_tx_sender(self):
        sender="0x"+"11"*20
        txhash="0x"+"55"*32
        ev={"transactionHash":txhash,"topics":[c.TRANSFER,
             "0x"+"00"*12+c.BOOSTER[2:].lower(),
             "0x"+"00"*12+sender[2:]],
             "data":hex(2*10**18),"removed":False}
        def mock_rpc(url,method,params=()):
            if method=="eth_chainId":return "0x1"
            if method=="eth_getCode":return "0x6001"
            if method=="eth_blockNumber":return hex(100)
            if method=="eth_getLogs":return [ev] if int(params[0]["fromBlock"],16)==0 else []
            if method=="eth_getTransactionByHash":
                return {"from":sender,"to":c.BOOSTER,
                        "input":c.EARMARK+("00"*32)}
            if method=="eth_getTransactionReceipt":
                return {"status":"0x1","blockNumber":"0x1",
                        "gasUsed":hex(100000),"effectiveGasPrice":hex(10**9)}
            raise AssertionError(method)
        def mock_call(url,method):
            if method=="isShutdown()":return "0x"+encode(["bool"],[False]).hex()
            return "0x"+encode(["uint256"],[50 if method=="earmarkIncentive()" else 10]).hex()
        with patch.object(c,"rpc",side_effect=mock_rpc),patch.object(c,"ethcall",side_effect=mock_call):
            report=c.inspect("rpc")
        self.assertEqual(report["direct_earmark_calls_paid"],1)
        self.assertEqual(report["direct_paid_crv_total_units"],"2")
        self.assertEqual(report["gas_eth_total_for_paid_direct_calls"],"0.0001")

    def test_unknown_rpc_failure_never_zero(self):
        with patch.object(c,"rpc",side_effect=RuntimeError("unreachable")):
            with self.assertRaises(RuntimeError):c.inspect("rpc")

if __name__=="__main__":unittest.main()
