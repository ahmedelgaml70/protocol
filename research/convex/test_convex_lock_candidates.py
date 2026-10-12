import unittest
from unittest.mock import patch
from eth_abi import encode
import convex_lock_candidates as c
class CandidateTests(unittest.TestCase):
    def test_wrong_chain(self):
        with patch.object(c.ev,"rpc",return_value="0x89"):
            with self.assertRaisesRegex(RuntimeError,"Wrong chain"):
                c.get_candidates("bad")
    def test_block_binary_search(self):
        def fn(url,method,args):
            self.assertEqual(method,"eth_getBlockByNumber")
            n=int(args[0],16)
            return {"timestamp":hex(n*12)}
        with patch.object(c.ev,"rpc",side_effect=fn):
            self.assertEqual(c.block_at_or_before("u",3000000,2999999*12),2999999)
    def test_abi_first_pending_lock(self):
        r=encode(["uint112","uint112","uint32"],[10**18,0,12345])
        self.assertEqual(len(r),96)
    def test_cannot_send_sign_or_change(self):
        for method in ("eth_sendTransaction","eth_sendRawTransaction","eth_sign","personal_sign"):
            with self.assertRaises(ValueError):c.ev.rpc("bad",method,[])
if __name__=="__main__":unittest.main()
