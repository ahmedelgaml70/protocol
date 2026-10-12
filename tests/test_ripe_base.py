"""No RPC/network required to exercise Ripe keeper evidence guards."""
import unittest
from ripe_base import (AUCTION,GREEN,SGREEN,TELLER,TOPIC,TRANSFER,decode_liquidation,
                       transfer_rows,verify_transaction,chain_state,ZERO)

def abi(*args):return "0x"+"".join(f"{x:064x}" for x in args)
SENDER="0x"+"2"*40
HASH="0x"+"a"*64
LOG={"address":AUCTION,"topics":[TOPIC,abi(123)],
     "data":abi(100,200,50,1,70,20,0,10),
     "transactionHash":HASH,"blockNumber":"0x123"}
def erc20(token,fromaddr,receiver,raw):
    return {"address":token,"topics":[TRANSFER,
             "0x"+fromaddr[2:].rjust(64,"0"),"0x"+receiver[2:].rjust(64,"0")],
             "data":abi(raw)}
class FakeRPC:
    def rpc(self,m,p):
        if m=="eth_chainId":return hex(8453)
        if m=="eth_blockNumber":return hex(1000)
        if m=="eth_getCode":return "0x6001"
        if m=="eth_getTransactionByHash":return {"hash":HASH,"from":SENDER,"to":TELLER}
        if m=="eth_getTransactionReceipt":
            return {"status":"0x1","gasUsed":"0x64","effectiveGasPrice":"0x2","l1Fee":"0x5",
                    "logs":[LOG,erc20(SGREEN,ZERO,SENDER,77)]}
        raise AssertionError(m)

class Tests(unittest.TestCase):
    def test_event_fee_position(self):
        x=decode_liquidation(LOG)
        self.assertEqual(x["keeper_fee_raw"],"10")
        self.assertEqual(x["liquidated_user"],"0x"+f"{123:040x}")

    def test_wrong_event_rejected(self):
        l=dict(LOG);l["address"]=GREEN
        with self.assertRaises(ValueError):decode_liquidation(l)

    def test_savings_green_mint_paid(self):
        r=verify_transaction(FakeRPC(),HASH,[])
        self.assertEqual(r["savings_green_shares_direct_mint_raw"],"77")
        self.assertTrue(r["actual_payout_to_submitter_observed"])
        self.assertEqual(r["full_receipt_fee_wei"],"205")
        self.assertTrue(r["sent_directly_to_teller"])

    def test_transfer_not_to_submitter_ignored(self):
        l=[erc20(GREEN,ZERO,"0x"+"3"*40,15)]
        r=transfer_rows({"logs":l},SENDER)
        self.assertEqual(r["green_received_raw"],"0")


    def test_deployed_runtime_flags(self):
        class ConfigRPC(FakeRPC):
            def rpc(self,m,p):
                if m=="eth_call":
                    data=p[0]["data"]
                    if data=="0xb187bd26":return abi(0)
                    if data=="0x313ce567":return abi(18)
                    if data=="0x10c7afae":
                        return abi(32,1,100,0,10**20,150, 0,0,0,0,0, 352,352)
                return super().rpc(m,p)
        runtime=chain_state(ConfigRPC())["runtime"]
        self.assertTrue(runtime["liquidations_enabled"])
        self.assertFalse(runtime["AuctionHouse_is_paused"])
        self.assertEqual(runtime["keeper_fee_ratio_bps_config"],"100")
        self.assertEqual(runtime["SavingsGreen_decimals"],18)

    def test_all_current_manifest_contracts_have_bytecode(self):
        result=chain_state(FakeRPC())
        self.assertEqual(len(result["contracts"]),5)
        self.assertFalse(result["bytecode_matches_source_verified"])

if __name__=="__main__":unittest.main()
