.PHONY: help install run dev test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install project dependencies using poetry"
	@echo "  make run          - Run the application on port 3020"
	@echo "  make dev          - Run the application in development mode with auto-reload"
	@echo "  make test         - Run tests with pytest"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make lint         - Check code style with ruff and black"
	@echo "  make format       - Format code with black and fix with ruff"
	@echo "  make najie-dev    - Stop existing service and start in development mode"
	@echo "  make najie-stop   - Stop the running service on port 3020"
	@echo "  make clean        - Remove cache files and build artifacts"

install:
	poetry install

run:
	poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 3020

dev:
	poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 3020 --reload

test:
	poetry run pytest tests/ -v

coverage:
	poetry run coverage run -m pytest tests/
	poetry run coverage report
	poetry run coverage html

lint:
	poetry run ruff check .
	poetry run black --check .

format:
	poetry run black .
	poetry run ruff check --fix .

najie-dev:
	@echo "Stopping any running service on port 3020..."
	@-pkill -f "uvicorn.*3020" || true
	@sleep 2
	@echo "Starting service..."
	poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 3020

najie-stop:
	@echo "Stopping any running service on port 3020..."
	@-pkill -f "uvicorn.*3020" || true
	@sleep 2
	@echo "Service stopped."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov .coverage
