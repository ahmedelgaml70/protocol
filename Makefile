PYTHON ?= python3

.PHONY: help test scan history

help:
	@echo "Protocol — read-only bounty research"
	@echo "make test    - run offline unit tests"
	@echo "make scan    - scan recent Kerf RangeOrders (RPC required)"
	@echo "make history - read recent Kerf payout events (RPC required)"
	@echo "These commands do NOT sign or broadcast transactions."

test:
	$(PYTHON) -m unittest discover -s tests -v

scan:
	$(PYTHON) kerf_radar.py --max-orders 100 --output report.json

history:
	$(PYTHON) kerf_history.py --lookback-hours 24 --output history.json

.PHONY: multi-history
multi-history:
	$(PYTHON) kerf_multi_history.py --lookback-hours 24 --output multi_bounty_history.json

# Free, keyless read-only endpoint supports eth_call, eth_getCode, eth_estimateGas.
# It intentionally DOES NOT support eth_getLogs. Scan the 10 newest order IDs
# to remain well below the endpoint's shared 60-requests/minute ceiling.
.PHONY: scan-free
scan-free:
	$(PYTHON) kerf_radar.py --rpc https://triport.io/rpc/robinhood/public --max-orders 10 --output report.json

.PHONY: superfluid-receipts
superfluid-receipts:
	$(PYTHON) superfluid_receipts.py --output superfluid_receipts.json

.PHONY: superfluid-activity
superfluid-activity:
	$(PYTHON) superfluid_activity.py --network base-mainnet --days 30 --limit 300 --output superfluid_activity.json

.PHONY: superfluid-recent
superfluid-recent:
	$(PYTHON) superfluid_recent_receipts.py --activity evidence/superfluid-base-2026-10-11-activity-full.json --limit 12 --output superfluid_recent_receipts.json
