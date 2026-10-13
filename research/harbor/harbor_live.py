#!/usr/bin/env python3
"""Harbor Ethereum mainnet caller-bounty read-only preflight.

No signing, wallet, accounts or spend. Bounties are protocol-authorized and
receive a user-selected address; this script NEVER submits a transaction.
Amounts are in underlying wrapped collateral, NOT fiat dollars.
"""
import json,os,urllib.request,sys
from datetime import datetime,timezone
from decimal import Decimal
from Crypto.Hash import keccak

NETWORK=1
DUMMY="0x1111111111111111111111111111111111111111"
RPCS=("https://ethereum-rpc.publicnode.com","https://eth.llamarpc.com","https://eth.drpc.org")
# Official baofinance/harbor-docs static/integrators/addresses/mainnet-v1.json
# Five live markets with published StabilityPoolManager addresses, Oct 12 2026.
MARKETS={
 "eth-fxusd":("0xE39165aDE355988EFb24dA4f2403971101134CAB","0x7743e50F534a7f9F1791DdE7dCD89F7783Eefc39"),
 "btc-fxusd":("0x768E0a386e1972eB5995429Fe21E7aC0f22F516e","0x7743e50F534a7f9F1791DdE7dCD89F7783Eefc39"),
 "btc-steth":("0x5e9Bcaa1EDfD665c09a9e6693B447581d61A85A1","0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"),
 "usd-steth":("0x377a4A6BEC4C75F2B7054B67Df03ce9A7497c33d","0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"),
 "usd-wbtc":("0x2506223d01072f795487Ff1f67aD40E1D3B15De0","0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"),
}
RPC_ALLOW={"eth_chainId","eth_blockNumber","eth_getCode","eth_call","eth_estimateGas","eth_gasPrice"}
def selector(sig):
    h=keccak.new(digest_bits=256);h.update(sig.encode());return "0x"+h.digest()[:4].hex()
def rpc(url,method,params=()):
    if method not in RPC_ALLOW:raise ValueError("Mutating RPC blocked: "+method)
    req=urllib.request.Request(url,data=json.dumps({"jsonrpc":"2.0","id":1,
                   "method":method,"params":list(params)}).encode(),
                   headers={"Content-Type":"application/json",
                            "User-Agent":"ProtocolHarborReadonly/1.0"})
    with urllib.request.urlopen(req,timeout=15) as resp:data=json.load(resp)
    if "error" in data or "result" not in data:
        raise RuntimeError(method+": "+str(data.get("error","missing result"))[:160])
    return data["result"]
def query(url,contract,sig):
    res=rpc(url,"eth_call",[{"to":contract,"data":selector(sig)},"latest"])
    return int(res,16)
def calldata(sig,address,number=0):
    return selector(sig)+"0"*24+address[2:].lower()+format(number,"064x")
def check(url):
    if int(rpc(url,"eth_chainId"),16)!=NETWORK:raise RuntimeError("Wrong chain")
    block=int(rpc(url,"eth_blockNumber"),16)
    gas_price=int(rpc(url,"eth_gasPrice"),16)
    out=[]
    for name,(manager,wrapped) in MARKETS.items():
        item={"market":name,"manager":manager,"wrapped_collateral":wrapped,"status":"incomplete"}
        try:
            if rpc(url,"eth_getCode",[manager,"latest"]) in ("0x","0x0","0x00"):
                raise RuntimeError("Manager not deployed")
            dec=query(url,wrapped,"decimals()")
            if not 0<=dec<=24:raise ValueError("Suspicious token decimals")
            bounty_ratio=query(url,manager,"harvestBountyRatio()")
            harvestable=query(url,manager,"harvestable()")
            cut_ratio=query(url,manager,"harvestCutRatio()")
            rebalance_ratio=query(url,manager,"rebalanceBountyRatio()")
            rebalanceable=bool(query(url,manager,"rebalanceable()"))
            if bounty_ratio>10**18 or cut_ratio>10**18:raise ValueError("Invalid ratio > 100%")
            base=Decimal(10)**dec
            reward_raw=(harvestable*bounty_ratio)//10**18
            item.update({
              "status":"observed","wrapped_decimals":dec,
              "harvestable_wrapped_units":str(Decimal(harvestable)/base),
              "harvest_bounty_ratio_pct":str(Decimal(bounty_ratio)*100/Decimal(10**18)),
              "harvest_fee_ratio_pct":str(Decimal(cut_ratio)*100/Decimal(10**18)),
              "current_gross_harvest_bounty_wrapped_units":str(Decimal(reward_raw)/base),
              "rebalance_bounty_ratio_pct":str(Decimal(rebalance_ratio)*100/Decimal(10**18)),
              "rebalanceable":rebalanceable,
              "harvest_simulation":"not_attempted",
              "rebalance_simulation":"not_attempted",
            })
            if reward_raw>0:
                data=calldata("harvest(address,uint256)",DUMMY)
                item["harvest_simulation"]="incomplete"
                try:
                    rpc(url,"eth_call",[{"from":DUMMY,"to":manager,"data":data},"latest"])
                    item["harvest_simulation"]="success_not_execution"
                    try:
                        gas=int(rpc(url,"eth_estimateGas",[{"from":DUMMY,"to":manager,"data":data}]),16)
                        item["harvest_gas_estimate"]=gas
                        item["harvest_gas_price_gwei"]=str(Decimal(gas_price)/Decimal(10**9))
                        item["harvest_gas_cost_eth"]=str(Decimal(gas*gas_price)/Decimal(10**18))
                    except Exception as e:item["gas_estimation_error"]=str(e)[:180]
                except Exception as e:item["harvest_call_error"]=str(e)[:180]
            if rebalanceable and rebalance_ratio>0:
                data=calldata("rebalance(address,uint256)",DUMMY)
                item["rebalance_simulation"]="incomplete"
                try:
                    rpc(url,"eth_call",[{"from":DUMMY,"to":manager,"data":data},"latest"])
                    item["rebalance_simulation"]="success_not_execution"
                    try:
                        gas=int(rpc(url,"eth_estimateGas",[{"from":DUMMY,"to":manager,"data":data}]),16)
                        item["rebalance_gas_cost_eth"]=str(Decimal(gas*gas_price)/Decimal(10**18))
                    except Exception as e:item["rebalance_gas_error"]=str(e)[:180]
                except Exception as e:item["rebalance_call_error"]=str(e)[:180]
        except Exception as e:item["error"]=str(e)[:250]
        out.append(item)
    return {"utc":datetime.now(timezone.utc).isoformat(),"network":"Ethereum mainnet",
        "observed_block":block,"provider":url,"markets":out,
        "observed_markets":sum(x["status"]=="observed" for x in out),
        "positive_harvest_bounty_markets":sum(x["status"]=="observed" and Decimal(x["current_gross_harvest_bounty_wrapped_units"])>0 for x in out),
        "rebalance_possible_markets":sum(x["status"]=="observed" and x["rebalanceable"] for x in out),
        "limitations":"Live read-only current-state sample of five configured markets. Wrapped assets not cash or raw ETH, and rebalance bounty output token may be leveraged token; no USD pricing or competition odds. Simulation is not guaranteed mined or profitable.",
        "spent_usd":0,"realized_income_usd":0}
def main():
    os.makedirs("reports",exist_ok=True);attempts=[];report=None
    for url in RPCS:
        try:
            report=check(url)
            attempts.append({"provider":url,"status":"sampled"})
            if report["observed_markets"]>0:break
        except Exception as e:attempts.append({"provider":url,"status":"incomplete","error":str(e)[:210]})
    if report is None:report={"status":"incomplete","message":"No provider available; not proof of zero"}
    report["provider_attempts"]=attempts
    with open("reports/harbor_live.json","w") as f:json.dump(report,f,indent=2)
    print(json.dumps({k:report.get(k) for k in ("observed_block","observed_markets",
       "positive_harvest_bounty_markets","rebalance_possible_markets","markets","provider_attempts")},indent=2))
    return 0 if report.get("observed_markets",0)>0 else 2
if __name__=="__main__":sys.exit(main())
