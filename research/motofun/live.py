#!/usr/bin/env python3
"""moto.fun mainnet graduation reward census. GET and eth_call only, no keys."""
import json, os, urllib.request, time, sys
from decimal import Decimal
from datetime import datetime,timezone
from Crypto.Hash import keccak

API="https://api.motoswap.org"
# Fallback ONLY after /config fails; first-party https://docs.motoswap.org/dev/addresses
DOCUMENTED_ADDRESSES={"launchpadCurve":"0xb65b67e986d7B097652920d72202F2c78319BC2C",
  "launchpadLens":"0xb631697124c8e6Bb6C221Cc017e47D4168bd3411"}
RPCLIST=("https://ethereum-rpc.publicnode.com","https://eth.drpc.org")
ALLOW_PATHS={"/config","/motofun/stats","/motofun/coins?limit=100"}
READ_METHODS={"eth_chainId","eth_blockNumber","eth_getCode","eth_call","eth_estimateGas","eth_gasPrice"}
ZERO="0x"+"0"*40
DUMMY="0x"+"1"*40
LIMIT=100
MAX_PAGES=3
def sel(sig):
 h=keccak.new(digest_bits=256);h.update(sig.encode());return "0x"+h.digest()[:4].hex()
def address(x):
 return isinstance(x,str) and len(x)==42 and x[:2]=="0x" and all(v in "0123456789abcdefABCDEF" for v in x[2:])
def get_json(path):
 if path not in ALLOW_PATHS:raise ValueError("GET path is not allowlisted")
 req=urllib.request.Request(API+path,method="GET",headers={"Accept":"application/json","User-Agent":"ProtocolResearchReadonly/1.0"})
 with urllib.request.urlopen(req,timeout=20) as response:
  data=json.load(response)
 if not isinstance(data,dict):raise ValueError("Invalid top-level JSON")
 return data
def rpc(url,method,params=()):
 if method not in READ_METHODS:raise ValueError("RPC write/sign blocked: "+method)
 body=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":list(params)}).encode()
 req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json","User-Agent":"ProtocolResearchReadonly/1.0"})
 with urllib.request.urlopen(req,timeout=18) as response: data=json.load(response)
 if "error" in data or "result" not in data:raise RuntimeError(str(data.get("error","missing result"))[:180])
 return data["result"]
def word_address(sig,addr):return sel(sig)+("0"*24)+addr[2:].lower()
def inspect(config,stats,coins,url):
 if int(rpc(url,"eth_chainId"),16)!=1:raise ValueError("wrong Ethereum chain")
 addrs=config.get("addresses",{})
 curve=addrs.get("launchpadCurve")
 lens=addrs.get("launchpadLens")
 if not address(curve) or not address(lens):raise ValueError("bad official dynamic deployment addresses")
 if not config.get("motofunEnabled") or curve.lower()==ZERO or lens.lower()==ZERO:
  return {"status":"official_api_reports_disabled","coin_counts":{}}
 if rpc(url,"eth_getCode",[curve,"latest"]) in ("0x","0x0"):raise RuntimeError("No curve bytecode")
 if rpc(url,"eth_getCode",[lens,"latest"]) in ("0x","0x0"):raise RuntimeError("No lens bytecode")
 block=int(rpc(url,"eth_blockNumber"),16)
 found=[];counts={};errors=[]
 for i,token in enumerate(coins):
  if not isinstance(token,dict):continue
  value=str(token.get("status") or token.get("lifecycle") or "unknown")
  counts[value]=counts.get(value,0)+1
  if value.lower() not in ("frozen","locked"):continue
  addr=token.get("address") or token.get("tokenAddress") or token.get("token")
  if not address(addr):errors.append({"row":i,"reason":"Frozen status but missing token address"});continue
  obj={"token":addr,"api_status":value,"graduation":"incomplete"}
  try:
   payload=word_address("graduationReadiness(address)",addr)
   raw=rpc(url,"eth_call",[{"to":lens,"data":payload},"latest"])
   data=bytes.fromhex(raw[2:])
   if len(data)!=224:raise ValueError("graduationReadiness returned wrong ABI length")
   v=[int.from_bytes(data[j:j+32],"big") for j in range(0,224,32)]
   obj.update({"regime":v[0],"ready_at_unix":v[1],
               "gross_bounty_eth":str(Decimal(v[5])/Decimal(10**18)),
               "sells_open_unix":v[6],
               "graduation":"lens_success"})
   if v[0]==0 and v[5]>0:  # Official enum Ready = 0
    args={"from":DUMMY,"to":curve,"data":word_address("graduate(address)",addr)}
    try:
     rpc(url,"eth_call",[args,"latest"])
     obj["simulate"]="success_not_transaction"
     try:
      gas=int(rpc(url,"eth_estimateGas",[args]),16)
      wei=int(rpc(url,"eth_gasPrice"),16)
      obj["gas_estimate"]=gas;obj["gas_price_gwei"]=str(Decimal(wei)/Decimal(10**9))
      obj["gross_minus_gas_eth"]=str(Decimal(v[5]-gas*wei)/Decimal(10**18))
     except Exception as e:obj["estimate_error"]=str(e)[:200]
    except Exception as e:obj["simulate"]="revert_or_incomplete";obj["simulate_error"]=str(e)[:190]
  except Exception as e:obj["error"]=str(e)[:200]
  found.append(obj)
 return {"status":"bounded_mainnet_venue_census","block":block,"curve":curve,"lens":lens,
   "official_api_enabled":True,"open_phase":config.get("launchPhase"),
   "coin_rows_scanned":len(coins),"api_coin_status_counts":counts,
   "frozen_coins":found,"errors":errors,"venue_stats_keys":list(stats.keys())[:30],
   "warning":"API coin sample not necessarily complete; dynamic deployed contracts and read-only lens checked. Only Ready regime simulates, no txs signed or sent. Competition/price not proven."}
def main():
 os.makedirs("reports",exist_ok=True)
 report={"utc":datetime.now(timezone.utc).isoformat(),
         "cash_spent":0,"cash_earned":0,"source":"official MotoSwap REST + Ethereum eth_call"}
 try:
  cfg=get_json("/config")
  report["config_status"]="ok"
  report["config_enabled"]=cfg.get("motofunEnabled")
 except Exception as e:
  cfg=None;report["config_status"]="incomplete";report["config_error"]=str(e)[:200]
 try:
  stats=get_json("/motofun/stats")
  report["stats_status"]="ok"
  report["stats_summary"]={k:v for k,v in stats.items() if isinstance(v,(int,float,bool)) or (isinstance(v,str) and len(v)<30)}
 except Exception as e:
  stats={};report["stats_status"]="incomplete";report["stats_error"]=str(e)[:200]
 try:
  board=get_json("/motofun/coins?limit=100")
  coins=board.get("items") or board.get("coins") or []
  if not isinstance(coins,list):raise ValueError("bad coins list")
  report["coins_status"]="ok"
  report["first_page_size"]=len(coins)
  report["has_more"]=bool(board.get("hasMore") or board.get("nextCursor"))
  report["pagination_warning"]="first page only; additional pages require opaque signed cursor" if report["has_more"] else None
 except Exception as e:
  coins=[];report["coins_status"]="incomplete";report["coins_error"]=str(e)[:200]
 if cfg is None and report["stats_status"]=="ok":
  cfg={"addresses":DOCUMENTED_ADDRESSES,"motofunEnabled":True,"launchPhase":"unknown_due_config_404"}
  report["config_fallback"]="first_party_docs_address_static_and_verifies_live_bytecode"
 if cfg is not None:
  tries=[]
  for url in RPCLIST:
   try:report["live"]=inspect(cfg,stats,coins,url);report["live"]["provider"]=url;break
   except Exception as e:tries.append({"provider":url,"error":str(e)[:240]})
  else:report["live"]={"status":"incomplete","reason":"no public Ethereum RPC provider succeeded"}
  report["rpc_attempts"]=tries
 with open("reports/motofun-live.json","w") as f:json.dump(report,f,indent=2)
 print(json.dumps(report,indent=2)[:28000])
 return 0 if report.get("live",{}).get("status") in ("bounded_mainnet_venue_census","official_api_reports_disabled") else 2
if __name__=="__main__":sys.exit(main())
