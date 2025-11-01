.PHONY: install run dev test lint format clean

install:
	poetry install

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

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

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov .coverage
