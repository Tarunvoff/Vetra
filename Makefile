.PHONY: install dev test lint format run-sim run-live benchmark dashboard clean docker-up docker-down doctor

install:
	pip install -e .

dev:
	pip install -e ".[dev,simulation,telemetry]"

test:
	pytest -v --cov=kvguard tests/

test-unit:
	pytest -v tests/unit/

test-integration:
	pytest -v tests/integration/

lint:
	ruff check kvguard/ tests/ benchmarks/

format:
	ruff format kvguard/ tests/ benchmarks/

doctor:
	python -m kvguard.cli.main doctor

run-sim:
	python -m kvguard.cli.main start --mode simulation --port 8080

run-live:
	python -m kvguard.cli.main start --mode live --vllm-url http://localhost:8000 --port 8080

benchmark:
	python benchmarks/runners/kvguard.py --workload mixed --requests 50

dashboard:
	cd dashboard && npm run dev

docker-up:
	docker compose up -d

docker-down:
	docker compose down

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .coverage htmlcov/ .ruff_cache/
