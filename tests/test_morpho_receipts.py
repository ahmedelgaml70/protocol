"""Morpho receipt checker tests: controlled synthetic RPC, no network."""
import unittest
from morpho_receipts import MORPHO,TOPIC,audit,verify_one

TX="0x"+"a"*64
MKT="0x"+"b"*64
CALLER="0x"+"2"*40
SUBMIT="0x"+"3"*40
def abi(*nums): return "0x"+"".join(f"{n:064x}" for n in nums)
def event():
    return {"tx_hash":TX,"market_id":MKT,"indexed_liquidator":CALLER,
            "log_index":6,"repaidAssets_raw":"200","seizedAssets_raw":"240",
            "badDebtAssets_raw":"0"}
class FakeRPC:
    def rpc(self,m,p):
        if m=="eth_chainId":return hex(8453)
        if m=="eth_getTransactionByHash":return {"hash":TX,"from":SUBMIT,"to":CALLER}
        if m=="eth_getTransactionReceipt":
            return {"status":"0x1","gasUsed":"0x64","effectiveGasPrice":"0x4",
                    "l1Fee":"0x5","logs":[{"logIndex":"0x6","address":MORPHO,
                    "topics":[TOPIC,MKT,abi(2),abi(4)],
                    "data":abi(200,201,240,0,0)}]}
        raise AssertionError(m)
class Tests(unittest.TestCase):
    def test_receipt_matches_indexed_event_without_pnl(self):
        out=audit(FakeRPC(),{"chain_id":8453,"events":[event()]},1)
        self.assertEqual(out["validated_tx_count"],1)
        self.assertEqual(out["rows"][0]["full_gas_wei"],"405")
        self.assertTrue(out["rows"][0]["onchain_liquidator_may_differ_from_tx_submitter"])
        self.assertFalse(out["realized_usd_profit_verified"])
    def test_bad_seized_amount_detected(self):
        bad=event();bad["seizedAssets_raw"]="99999"
        out=audit(FakeRPC(),{"chain_id":8453,"events":[bad]},1)
        self.assertEqual(out["validated_tx_count"],0)
        self.assertEqual(len(out["receipt_errors"]),1)
    def test_wrong_chain_rejected(self):
        with self.assertRaises(ValueError):
            audit(FakeRPC(),{"chain_id":1,"events":[event()]},1)
if __name__=="__main__":unittest.main()
