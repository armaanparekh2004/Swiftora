PYTHON=python
PIP=pip

.PHONY: run test lint

run:
	@echo "Starting Swiftora backend on http://localhost:8000"
	@$(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	@$(PYTHON) -m pytest -q

lint:
	@echo "No linter configured.  Add flake8 or similar if desired."