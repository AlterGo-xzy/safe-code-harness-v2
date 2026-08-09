PYTHON ?= python3
NPM ?= npm

.PHONY: test backend-test frontend-test demos

test: backend-test frontend-test

backend-test:
	$(PYTHON) -m pytest backend/tests

frontend-test:
	$(NPM) --prefix frontend test

demos:
	$(PYTHON) scripts/run_guardrail_demo.py
	$(PYTHON) scripts/run_feedback_demo.py
	$(PYTHON) scripts/run_approval_demo.py
