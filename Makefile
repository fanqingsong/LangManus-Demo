.PHONY: install dev test lint format clean serve

# Install dependencies
install:
	uv sync

# Install with dev dependencies
dev:
	uv sync --dev

# Run tests
test:
	uv run pytest

# Run tests with coverage
coverage:
	uv run pytest --cov=src --cov-report=html --cov-report=term

# Lint code
lint:
	uv run flake8 src tests
	uv run mypy src

# Format code
format:
	uv run black src tests
	uv run isort src tests

# Clean build artifacts
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Start the API server
serve:
	uv run server.py

# Run the main application
run:
	uv run main.py

# Run Streamlit app
streamlit:
	uv run streamlit run streamlit_app.py 