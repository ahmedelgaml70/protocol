import unittest
from unittest.mock import patch
from eth_abi import encode
import keep3r_funding as p

class Keep3rTests(unittest.TestCase):
    def test_method_selectors(self):
        self.assertEqual(p.selector("transfer(address,uint256)"),"0xa9059cbb")

    def test_no_wallet_or_mutating_methods(self):
        for method in ("eth_sendTransaction","eth_sendRawTransaction",
                       "personal_sign","eth_sign","eth_signTypedData_v4"):
            with self.subTest(method=method):
                with self.assertRaisesRegex(ValueError,"Unauthorized"):
                    p.rpc("https://example.invalid",method,[])

    def test_wrong_chain_disallowed(self):
        with patch.object(p,"rpc",return_value="0x89"):
            with self.assertRaisesRegex(RuntimeError,"Wrong chain"):
                p.scan("rpc")

    def test_credits_are_not_marked_claimable(self):
        def dummy(url,method,params=()):
            if method=="eth_chainId":return "0x1"
            if method=="eth_getCode":return "0x6001"
            if method=="eth_blockNumber":return "0x999"
            raise AssertionError(method)
        def dummy_view(url,signature,argtypes=None,values=None):
            if signature=="jobs()":return encode(["address[]"],[["0x"+"11"*20]])
            if signature=="totalJobCredits(address)":return encode(["uint256"],[100*10**18])
            if signature=="workedAt(address)":return encode(["uint256"],[123])
            if signature=="jobTokenCredits(address,address)":return encode(["uint256"],[0])
            raise AssertionError(signature)
        with patch.object(p,"rpc",side_effect=dummy),patch.object(p,"view",side_effect=dummy_view):
            report=p.scan("rpc")
        self.assertEqual(report["funded_jobs_in_scanned_set"],1)
        self.assertEqual(report["verified_income_usd"],0)
        self.assertEqual(report["status"],"funding_observation_not_claimability")

    def test_failure_never_fake_zero(self):
        with patch.object(p,"rpc",side_effect=RuntimeError("RPC down")):
            with self.assertRaisesRegex(RuntimeError,"RPC down"):
                p.scan("rpc")

if __name__=="__main__":unittest.main()
