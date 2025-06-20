.PHONY: install install-pip dev test lint format clean serve setup

# Install dependencies using uv (recommended)
install:
	uv sync

# Install dependencies using pip
install-pip:
	pip install -r requirements.txt

# Install with dev dependencies
dev:
	uv sync --dev

# Install dev dependencies with pip
dev-pip:
	pip install -r requirements.txt -r requirements-dev.txt

# Setup project (copy .env.example to .env)
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file from .env.example"; \
		echo "📝 Please edit .env with your API keys"; \
	else \
		echo "⚠️  .env file already exists"; \
	fi

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