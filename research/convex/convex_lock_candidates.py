#!/usr/bin/env python3
"""Small timestamp-anchored, read-only sample of Convex locker expired accounts.

Sampling old deposit accounts is NOT a complete enumeration of kickable wallets.
Only eth_call + eth_estimateGas, no signing or transaction is supported.
"""
import json,os,sys
from datetime import datetime,timezone
from eth_abi import decode,encode
from eth_utils import keccak
import convex_earmark as ev
import convex_kicks as kick

AGE_DAYS=(160,205,270)
WINDOW_BLOCKS=320
CHUNK=160
MAX_STAKERS=36
USER_TOPIC="0x"+keccak(text="Staked(address,uint256,uint256,uint256,uint256)").hex()
SENDER="0x1111111111111111111111111111111111111111"

def call(url,signature,types=None,values=None):
    data=ev.sel(signature)+ (encode(types,values).hex() if types else "")
    ans=ev.rpc(url,"eth_call",[{"to":kick.LOCKER,"data":data},"latest"])
    return bytes.fromhex(ans[2:])

def block_at_or_before(url,tip,target):
    lo,hi=max(0,tip-2700000),tip
    def stamp(b):
        x=ev.rpc(url,"eth_getBlockByNumber",[hex(b),False])
        if not x:raise RuntimeError("Archive block unavailable")
        return int(x["timestamp"],16)
    if stamp(lo)>target:raise RuntimeError("Historical target before available archive window")
    while lo<hi:
        m=(lo+hi+1)//2
        if stamp(m)<=target:lo=m
        else:hi=m-1
    return lo

def get_candidates(url):
    if int(ev.rpc(url,"eth_chainId"),16)!=1:raise RuntimeError("Wrong chain")
    if ev.rpc(url,"eth_getCode",[kick.LOCKER,"latest"]) in ("0x","0x0","0x00"):
        raise RuntimeError("Locker bytecode missing")
    tip=int(ev.rpc(url,"eth_blockNumber"),16)
    tipblock=ev.rpc(url,"eth_getBlockByNumber",[hex(tip),False])
    now=int(tipblock["timestamp"],16)
    reward_rate=kick.read_param(url,"kickRewardPerEpoch()")
    grace_epochs=kick.read_param(url,"kickRewardEpochDelay()")
    epoch=kick.read_param(url,"rewardsDuration()")
    samples=[];addresses={}
    for days in AGE_DAYS:
        try:
            anchor=block_at_or_before(url,tip,now-days*86400)
            start=max(0,anchor-WINDOW_BLOCKS+1)
            logs=[]
            for b in range(start,anchor+1,CHUNK):
                logs+=ev.rpc(url,"eth_getLogs",[{"address":kick.LOCKER,
                    "fromBlock":hex(b),"toBlock":hex(min(anchor,b+CHUNK-1)),
                    "topics":[USER_TOPIC]}])
            samples.append({"age_days":days,"start":start,"end":anchor,"status":"complete",
                            "staked_events":len(logs)})
            for x in logs:
                if len(x["topics"])>1:
                    address="0x"+x["topics"][1][-40:]
                    addresses[address.lower()]=address
        except Exception as e:
            samples.append({"age_days":days,"status":"incomplete","error":str(e)[:200]})
    checked=[];candidates=[]
    for address in list(addresses.values())[:MAX_STAKERS]:
        try:
            bal=decode(["uint112","uint112","uint32"],call(url,"balances(address)",["address"],[address]))
            locked=int(bal[0]);nxt=int(bal[2])
            item={"address":address,"locked_cvx_units":str(locked/10**18),
                  "next_unlock_index":nxt,"status":"no_pending_lock"}
            if locked:
                raw=call(url,"userLocks(address,uint256)",["address","uint256"],[address,nxt])
                amount,boosted,unlock=decode(["uint112","uint112","uint32"],raw)
                item["first_unprocessed_lock_cvx_units"]=str(amount/10**18)
                item["first_unprocessed_unlock_unix"]=unlock
                eligible=unlock+grace_epochs*epoch<=now and amount>0
                item["maturity_gate_open"]=eligible
                item["status"]="matured_screened" if eligible else "not_matured"
                if eligible:
                    data=ev.sel("kickExpiredLocks(address)")+encode(["address"],[address]).hex()
                    call_args={"from":SENDER,"to":kick.LOCKER,"data":data}
                    try:
                        ev.rpc(url,"eth_call",[call_args,"latest"])
                        item["simulation"]="success_only_not_guaranteed"
                        try:item["estimated_gas"]=int(ev.rpc(url,"eth_estimateGas",[call_args]),16)
                        except Exception as e:item["gas_error"]=str(e)[:200]
                        candidates.append(item)
                    except Exception as e:item["simulation"]="reverted:"+str(e)[:160]
            checked.append(item)
        except Exception as e:
            checked.append({"address":address,"status":"incomplete","error":str(e)[:200]})
    done=sum(x["status"]=="complete" for x in samples)
    return {"status":"bounded_candidate_sample" if done else "incomplete",
      "at_utc":datetime.now(timezone.utc).isoformat(),"chain":1,"locker":kick.LOCKER,
      "rate_bps_per_overdue_epoch":reward_rate,"grace_epochs":grace_epochs,"epoch_seconds":epoch,
      "sample_windows":samples,"unique_staking_accounts_in_sample":len(addresses),
      "sampled_accounts":len(checked),"mature_and_simulated_success_count":len(candidates),
      "candidates":candidates,"accounts":checked,
      "scope":"Three tiny noncontiguous historical Staked-event windows. Extremely sparse and strongly biased. A successful eth_call and gas estimate are not guaranteed reward, and no CVX transfer or USD net is proven. User-owned address not required.",
      "capital_spent_usd":0,"user_earnings_usd":0}
def main():
    os.makedirs("reports",exist_ok=True)
    attempts=[];result=None
    for url in ev.PROVIDERS:
        try:
            result=get_candidates(url)
            attempts.append({"url":url,"status":result["status"]})
            if result["status"]!="incomplete":break
        except Exception as e:attempts.append({"url":url,"status":"incomplete","error":str(e)[:180]})
    if result is None:result={"status":"incomplete"}
    result["attempts"]=attempts
    with open("reports/convex-current-lock-sample.json","w") as f:json.dump(result,f,indent=2)
    print(json.dumps({k:result.get(k) for k in ("status","rate_bps_per_overdue_epoch",
      "grace_epochs","sample_windows","unique_staking_accounts_in_sample",
      "sampled_accounts","mature_and_simulated_success_count","candidates","attempts")},indent=2))
    return 0 if result["status"]!="incomplete" else 2
if __name__=="__main__":sys.exit(main())
