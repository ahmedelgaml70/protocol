"""Offline ABI and payout-reward tests, no blockchain access required."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pooltogether_claim_history as m


def abi(*xs):
    return "0x"+"".join(f"{int(x):064x}" for x in xs)


def example(fee=10**18):
    return {
        "address":m.PRIZE_POOL,
        "topics":[m.TOPIC,abi(123),abi(456),abi(456)],
        "data":abi(727,2,4,10**20,fee,789),
        "transactionHash":"0x"+"f"*64,
        "blockNumber":"0x123"
    }


class FakeRPC:
    def rpc(self,method,params):
        if method=="eth_getTransactionByHash":
            return {"from":"0x"+f"{789:040x}", "to":m.CLAIMER}
        if method=="eth_getTransactionReceipt":
            return {"status":"0x1","gasUsed":"0x64","effectiveGasPrice":"0x2","l1Fee":"0x5"}
        raise AssertionError(method)


class ClaimTests(unittest.TestCase):
    def test_decode_reward(self):
        row=m.decode_claim(example())
        self.assertEqual(row["claim_reward_raw"],str(10**18))
        self.assertEqual(row["draw_id"],727)
        self.assertEqual(row["reward_recipient"],"0x"+f"{789:040x}")

    def test_reward_recipient_and_gas(self):
        row=m.decode_claim(example())
        result=m.summarize([row],18,100,200,"0x"+"a"*40)
        m.attach_receipt_samples(FakeRPC(),result,1)
        self.assertEqual(result["total_accrued_claim_reward_in_prize_tokens"],"1")
        self.assertEqual(result["receipt_samples"][0]["network_fee_wei"],"205")
        self.assertTrue(result["receipt_samples"][0]["fee_recipient_is_submitter"])
        self.assertTrue(result["receipt_samples"][0]["sent_to_published_current_claimer"])
        self.assertFalse(result["profit_usd_verified"])

    def test_priority_zero_fee(self):
        r=m.summarize([m.decode_claim(example(0))],18,1,2,"0x"+"a"*40)
        self.assertEqual(r["events_with_positive_claim_reward"],0)

    def test_bad_log_rejected(self):
        item=example()
        item["address"]="0x"+"e"*40
        with self.assertRaises(ValueError):
            m.decode_claim(item)


if __name__=="__main__":
    unittest.main()
