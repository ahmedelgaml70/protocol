"""Offline proof checks; no GraphQL or Base RPC live calls."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pooltogether_subgraph import select_tx_hashes, verify_receipt, PRIZE_POOL, TOPIC, CLAIMER


def abi(*xs):return "0x" + "".join(f"{int(x):064x}" for x in xs)

class FakeRPC:
    def rpc(self, method, params):
        txhash=params[0]
        if method=="eth_getTransactionByHash":
            return {"hash":txhash,"from":"0x"+f"{2:040x}","to":CLAIMER}
        if method=="eth_getTransactionReceipt":
            return {"status":"0x1","gasUsed":"0x64","effectiveGasPrice":"0x3","l1Fee":"0x2",
                    "logs":[{"address":PRIZE_POOL,
                             "topics":[TOPIC,abi(1),abi(2),abi(3)],
                             "data":abi(10,2,1,100000000,25000000,2),
                             "transactionHash":txhash,"blockNumber":"0x1"}]}
        raise AssertionError(method)

class SubgraphTests(unittest.TestCase):
    def test_deduplicate(self):
        h="0x"+"a"*64
        sample=[{"txHash":h,"timestamp":"1000","claimReward":"1"},
                {"txHash":h,"timestamp":"1000","claimReward":"3"}]
        got,count=select_tx_hashes(sample,900,10)
        self.assertEqual(got,[h])
        self.assertEqual(count,1)

    def test_receipt_and_recipient(self):
        h="0x"+"a"*64
        result=verify_receipt(FakeRPC(),h,6)
        self.assertTrue(result["sent_to_published_current_claimer"])
        self.assertTrue(result["fee_recipient_is_submitter"])
        self.assertEqual(result["event_claim_reward_tokens"],"25")
        self.assertEqual(result["network_fee_wei"],"302")

    def test_invalid_hash(self):
        with self.assertRaises(ValueError):
            select_tx_hashes([{"txHash":"evil","timestamp":"1000","claimReward":"1"}],900,5)

if __name__=="__main__":
    unittest.main()
