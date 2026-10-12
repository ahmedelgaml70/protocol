import unittest
from unittest.mock import patch
from eth_abi import encode
from eth_utils import keccak
import splits_observer as p

class TestObserver(unittest.TestCase):
    def test_event_topics_and_selector(self):
        self.assertEqual(p.selector("transfer(address,uint256)"),"0xa9059cbb")
        self.assertEqual(p.topic("Transfer(address,address,uint256)"),
          "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef")
    def test_no_mutating_rpc_methods(self):
        with self.assertRaisesRegex(ValueError,"blocked"):
            p.rpc("https://example.invalid","eth_sendRawTransaction",["0x"])
        with self.assertRaisesRegex(ValueError,"blocked"):
            p.rpc("https://example.invalid","eth_sendTransaction",[])
    def test_split_tuple_roundtrip(self):
        s=(["0x"+"11"*20,"0x"+"22"*20],[3,7],10,65000)
        from eth_abi import decode
        t=decode([p.SPLIT],encode([p.SPLIT],[s]))[0]
        self.assertEqual(tuple(t[1]),(3,7))
        self.assertEqual(t[3],65000)
        self.assertEqual(keccak(encode([p.SPLIT],[t])),
                         keccak(encode([p.SPLIT],[s])))
    def test_provider_failure_not_reported_as_zero(self):
        with patch.object(p,"assert_chain_and_code",side_effect=RuntimeError("blocked logs")):
            with self.assertRaisesRegex(RuntimeError,"blocked logs"):
                p.scan("https://example.invalid")

if __name__=="__main__":
    unittest.main()
