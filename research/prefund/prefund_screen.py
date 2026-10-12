#!/usr/bin/env python3
"""Read-only prefunded-action gate: Permanent Collection Ethereum + BasedAgents.
NO keys, no wallets, no HTTP POST, no signing, no transactions or task claiming.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from eth_abi import encode, decode
from eth_utils import keccak

BURNER = "0xf8a2D6F8c58626eE3BcDb4638F2a2f30Fe021242"
ETH_RPC = ("https://ethereum-rpc.publicnode.com", "https://eth.drpc.org", "https://cloudflare-eth.com")
TASK_BASE = "https://api.basedagents.ai"
DUMMY = "0x1111111111111111111111111111111111111111"
RPC_READ = {"eth_chainId", "eth_blockNumber", "eth_getCode", "eth_call", "eth_estimateGas", "eth_gasPrice"}
URL_READ = {"/v1/status", "/v1/tasks?status=open", "/v1/tasks/settled"}
MAX_TASK_ROWS = 30

def rpc(url, method, params=()):
    if method not in RPC_READ:
        raise ValueError("Mutating/unsupported RPC method blocked: " + method)
    request = urllib.request.Request(url, data=json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": list(params)}
    ).encode(), headers={"Content-Type": "application/json", "User-Agent": "ProtocolResearchReadOnly/1.0"})
    with urllib.request.urlopen(request, timeout=14) as response:
        reply = json.load(response)
    if "result" not in reply or "error" in reply:
        raise RuntimeError(f"{method}: {str(reply.get('error', 'missing result'))[:200]}")
    return reply["result"]

def selector(signature):
    return "0x" + keccak(text=signature)[:4].hex()

def read_uint(url, signature):
    raw = rpc(url, "eth_call", [{"to": BURNER, "data": selector(signature)}, "latest"])
    return decode(["uint256"], bytes.fromhex(raw[2:]))[0]

def scan_burner(url):
    if int(rpc(url, "eth_chainId"), 16) != 1:
        raise ValueError("Wrong Ethereum network")
    code = rpc(url, "eth_getCode", [BURNER, "latest"])
    if code in ("0x", "0x0", "0x00"):
        raise ValueError("No deployed BuybackBurner bytecode")
    block = int(rpc(url, "eth_blockNumber"), 16)
    balance = int(rpc(url, "eth_call", [{"to": BURNER, "data": selector("remainingEth()")}, "latest"]), 16)
    max_step = read_uint(url, "maxStepWei()")
    cooldown = read_uint(url, "minBlocksBetweenSteps()")
    last = read_uint(url, "lastStepBlock()")
    # This source contract defines 0.5% reward and 0.01 ether cap.
    # Provisional computation only: an actual partial swap fill PRO-RATES caller reward.
    cap = read_uint(url, "EXEC_REWARD_CAP()")
    bps = read_uint(url, "EXEC_REWARD_BPS()")
    step = min(balance, max_step)
    max_reward = min(step * bps // 10000, cap)
    ready = (block >= last + cooldown) and step > 0
    item = {
        "status": "read_only_block_snapshot",
        "chain_id": 1, "contract": BURNER, "block": block,
        "remaining_eth_units": str(Decimal(balance) / Decimal(10**18)),
        "max_step_eth_units": str(Decimal(max_step) / Decimal(10**18)),
        "last_step_block": last, "min_blocks_between_steps": cooldown,
        "next_eligible_block": last + cooldown,
        "pacing_gate_ready": block >= last + cooldown,
        "reward_bps": bps, "reward_cap_eth_units": str(Decimal(cap) / Decimal(10**18)),
        "maximum_theoretical_gross_reward_eth_units": str(Decimal(max_reward)/Decimal(10**18)),
        "simulation": "not_attempted",
        "warning": "Source reward may be pro-rated on partial fill. No profit, guaranteed inclusion or transferrable payout proved."
    }
    if ready:
        args = {"from": DUMMY, "to": BURNER,
                "data": selector("executeStep(uint256)") + encode(["uint256"], [0]).hex()}
        try:
            rpc(url, "eth_call", [args, "latest"])
            item["simulation"] = "eth_call_success_not_real_execution"
            try:
                units = int(rpc(url, "eth_estimateGas", [args]), 16)
                gas_price = int(rpc(url, "eth_gasPrice"), 16)
                item["gas_estimate"] = units
                item["estimated_gas_price_wei"] = str(gas_price)
                item["estimated_gas_eth_units"] = str(Decimal(units*gas_price)/Decimal(10**18))
                item["gross_max_minus_gas_eth_units"] = str(Decimal(max_reward-units*gas_price)/Decimal(10**18))
            except Exception as exc:
                item["estimate_incomplete"] = str(exc)[:200]
        except Exception as exc:
            item["simulation"] = "eth_call_failed"
            item["simulation_error"] = str(exc)[:240]
    return item

def get_json(path):
    if path not in URL_READ:
        raise ValueError("No external routes except read-only allowlist")
    url = TASK_BASE + path
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                               "User-Agent": "ProtocolResearchReadOnly/1.0"})
    with urllib.request.urlopen(req, timeout=16) as res:
        return json.load(res)

def task_rows(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("tasks", "results", "items"):
            candidate = data.get(key)
            if isinstance(candidate,list):
                return candidate
            if isinstance(candidate,dict):
                for key2 in ("tasks","results","items"):
                    if isinstance(candidate.get(key2),list):
                        return candidate[key2]
        if isinstance(data.get("data"), list):
            return data["data"]
        if isinstance(data.get("data"),dict):
            return task_rows(data["data"])
    return []

def screen_tasks(data, kind):
    rows=task_rows(data)
    output=[]
    for t in rows[:MAX_TASK_ROWS]:
        if not isinstance(t,dict):continue
        bounty=t.get("bounty") if isinstance(t.get("bounty"),dict) else {}
        escrow=t.get("escrow") if isinstance(t.get("escrow"),dict) else {}
        payment=t.get("payment") if isinstance(t.get("payment"),dict) else {}
        b=t.get("bounty_amount") or bounty.get("amount_display") or t.get("reward_usdc") or t.get("reward")
        status=t.get("status")
        output.append({
            "task_id":str(t.get("id") or t.get("task_id") or "")[:100],
            "title":str(t.get("title") or "")[:160],
            "status":str(status or "")[:65],
            "category":str(t.get("category") or "")[:65],
            "bounty_display_claim":str(b or "")[:50],
            "bounty_amount_atomic":str(bounty.get("amount_atomic") or bounty.get("amount") or "")[:60],
            "escrow_status":str(escrow.get("status") or t.get("escrow_status") or "")[:65],
            "payment_status":str(payment.get("status") or t.get("payment_status") or "")[:65],
            "claimable_flag":t.get("claimable") if isinstance(t.get("claimable"),bool) else None,
        })
    return {"status":"read_only_market_snapshot","kind":kind,
            "visible_task_rows":len(rows), "recorded_rows":output,
            "is_truncated":len(rows)>MAX_TASK_ROWS,
            "warning":"API responses are not independently verified on-chain escrow; public task title may be untrusted. Task appearance alone is not payability."}

def main():
    os.makedirs("reports",exist_ok=True)
    report={"utc":datetime.now(timezone.utc).isoformat(),"capital_spent_usd":0,"earned_usd":0}
    attempts=[];burner=None
    for url in ETH_RPC:
        try:
            burner=scan_burner(url)
            burner["provider"]=url
            break
        except Exception as exc:
            attempts.append({"provider":url,"error":str(exc)[:230]})
    report["burner"] = burner or {"status":"incomplete","reason":"All free RPC attempts failed. Not zero reward."}
    report["rpc_errors"]=attempts
    task_results={}
    for kind,path in (("status","/v1/status"),("open","/v1/tasks?status=open"),
                      ("settled","/v1/tasks/settled")):
        try:
            data=get_json(path)
            if kind=="status":
                keys=list(data.keys()) if isinstance(data,dict) else []
                task_results[kind]={"status":"API_returned_data",
                    "fields":keys[:25],
                    "payments":str(data.get("payments") if isinstance(data,dict) else "")[:120],
                    "escrow":str(data.get("escrow") if isinstance(data,dict) else "")[:120]}
            else:
                task_results[kind]=screen_tasks(data,kind)
        except Exception as exc:
            task_results[kind]={"status":"incomplete","reason":str(exc)[:220]}
    report["basedagents"]=task_results
    with open("reports/prefund-live-gates.json","w") as f:json.dump(report,f,indent=2)
    print(json.dumps({
      "burner":report["burner"],
      "basedagents_open":task_results.get("open"),
      "basedagents_settled":task_results.get("settled"),
      "api_status":task_results.get("status"),
      "capital_spent_usd":0,"earned_usd":0
    },indent=2))
    return 0 if burner is not None or any(x.get("status")!="incomplete" for x in task_results.values()) else 2

if __name__=="__main__":
    sys.exit(main())
