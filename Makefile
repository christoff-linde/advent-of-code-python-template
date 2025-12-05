.PHONY: scaffold download solve run all test benchmark benchmark-all lint format clean help

help:
	@echo "Advent of Code Python - Available Commands"
	@echo ""
	@echo "  make scaffold day=N         Scaffold a new day (with --download)"
	@echo "  make download day=N         Download input and puzzle for a day"
	@echo "  make solve day=N            Run solution for a specific day"
	@echo "  make run                    Run all solutions"
	@echo "  make test                   Run unit tests"
	@echo "  make benchmark day=N        Benchmark a specific day"
	@echo "  make benchmark-all          Benchmark all days"
	@echo "  make lint                   Check code style with ruff"
	@echo "  make format                 Format code with ruff"
	@echo "  make clean                  Remove cache and temp files"
	@echo ""

scaffold:
	@if [ -z "$(day)" ]; then echo "Usage: make scaffold day=N"; exit 1; fi
	uv run python main.py scaffold $(day) --download

download:
	@if [ -z "$(day)" ]; then echo "Usage: make download day=N"; exit 1; fi
	uv run python main.py download $(day)

solve:
	@if [ -z "$(day)" ]; then echo "Usage: make solve day=N"; exit 1; fi
	uv run python main.py solve $(day)

run:
	uv run python main.py all

test:
	uv run pytest -v

benchmark:
	@if [ -z "$(day)" ]; then echo "Usage: make benchmark day=N"; exit 1; fi
	uv run pytest */tests/test_day$(shell printf "%02d" $(day)).py -m benchmark --benchmark-only

benchmark-all:
	uv run pytest -m benchmark --benchmark-only

lint:
	uv run ruff check src/ */tests/ main.py

format:
	uv run ruff format src/ */tests/ main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	@echo "Cleaned cache and temp files"

.DEFAULT_GOAL := help
