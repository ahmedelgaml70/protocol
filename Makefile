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
	$(PYTHON) kerf_history.py --lookback-blocks 30000 --output history.json
