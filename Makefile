PYTHON ?= python

.PHONY: demos

demos:
	$(PYTHON) scripts/run_guardrail_demo.py
	$(PYTHON) scripts/run_feedback_demo.py
	$(PYTHON) scripts/run_approval_demo.py
