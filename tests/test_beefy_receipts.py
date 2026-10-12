"""Synthetic Base WETH receipts for Cowllector operator transactions."""
import unittest
from beefy_receipts import scan,WETH
from superfluid_receipts import TRANSFER

STRAT="0x"+"1"*40
SENDER="0x"+"2"*40
TX="0x"+"a"*64
def ev(amount):
    return {"address":WETH,"topics":[TRANSFER,"0x"+STRAT[2:].rjust(64,"0"),"0x"+SENDER[2:].rjust(64,"0")],
            "data":"0x"+f"{amount:064x}"}
class FakeRPC:
    def __init__(self,amount=1000):
        self.amount=amount
    def rpc(self,m,args):
        if m=="eth_chainId":return hex(8453)
        if m=="eth_getTransactionByHash":return {"hash":TX,"from":SENDER,"to":STRAT}
        if m=="eth_getTransactionReceipt":
            return {"status":"0x1","gasUsed":"0x64","effectiveGasPrice":"0x3","l1Fee":"0x2",
                    "logs":[ev(self.amount)]}
        raise AssertionError(m)
def activity():
    return {"recent_operator_harvest_sample":[
        {"chain":"base","operator_tx_hash_unverified":TX,
         "strategy_address":STRAT,"operator_transaction_ok":True}]}
class ReceiptTests(unittest.TestCase):
    def test_token_receipt_positive(self):
        o=scan(FakeRPC(),activity())
        self.assertEqual(o["receipt_rows"][0]["weth_received_by_submitter_raw"],"1000")
        self.assertEqual(o["receipt_rows"][0]["full_base_gas_fee_wei"],"302")
        self.assertEqual(o["conditional_positive_wnative_after_gas_count"],1)
        self.assertFalse(o["actual_realized_usd_profit_verified"])
    def test_negative_when_gas_larger(self):
        self.assertEqual(scan(FakeRPC(100),activity())["conditional_positive_wnative_after_gas_count"],0)
    def test_duplicates_are_deduplicated(self):
        a=activity()
        a["recent_operator_harvest_sample"]*=2
        self.assertEqual(scan(FakeRPC(),a)["reported_base_harvest_txs_selected"],1)
if __name__=="__main__":unittest.main()
