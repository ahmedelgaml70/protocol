import unittest
from unittest.mock import patch
import prefund_screen as p

class PrefundTests(unittest.TestCase):
    def test_forbid_broadcast_and_any_post_path(self):
        for method in ("eth_sendRawTransaction","eth_sendTransaction","personal_sign"):
            with self.assertRaisesRegex(ValueError,"blocked"):
                p.rpc("https://invalid",method,[])
        for path in ("/v1/tasks/claim","/v1/tasks","/v1/payments"):
            with self.assertRaisesRegex(ValueError,"allowlist"):
                p.get_json(path)
    def test_wrong_chain_no_evidence(self):
        with patch.object(p,"rpc",return_value="0x89"):
            with self.assertRaisesRegex(ValueError,"Wrong Ethereum"):
                p.scan_burner("rpc")
    def test_no_funds_no_call(self):
        state={"remainingEth()":0,"maxStepWei()":10**18,
               "minBlocksBetweenSteps()":5,"lastStepBlock()":95,
               "EXEC_REWARD_CAP()":10**16,"EXEC_REWARD_BPS()":50}
        def fake_rpc(url,method,args=()):
            if method=="eth_chainId":return "0x1"
            if method=="eth_getCode":return "0x6001"
            if method=="eth_blockNumber":return hex(100)
            if method=="eth_call":
                fn=args[0]["data"]
                for key,val in state.items():
                    if fn==p.selector(key):return '0x' + format(val,'064x')
                raise AssertionError("Should never call executeStep on zero funds")
            raise AssertionError(method)
        with patch.object(p,"rpc",side_effect=fake_rpc):
            result=p.scan_burner("rpc")
        self.assertEqual(result["simulation"],"not_attempted")
        self.assertEqual(result["maximum_theoretical_gross_reward_eth_units"],"0")
    def test_task_shape_readable(self):
        rows=[{"id":"task1","title":"Research","status":"open","claimable":True,
               "bounty":{"amount_display":"35","amount_atomic":"35000000"},
               "escrow":{"status":"funded"}}]
        x=p.screen_tasks({"tasks":rows},"open")
        self.assertEqual(x["visible_task_rows"],1)
        self.assertEqual(x["recorded_rows"][0]["escrow_status"],"funded")
        self.assertEqual(x["recorded_rows"][0]["interpreted_usdc"],"35")
        self.assertEqual(x["funded_open_at_least_25_usdc_count"],1)
        self.assertEqual(x["api_funded_open_declared_total_usdc"],"35")

if __name__=="__main__":
    unittest.main()
