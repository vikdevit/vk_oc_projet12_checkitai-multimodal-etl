.PHONY: install test lint format clean

# Installation du projet et des outils de développement
install:
	uv sync --extra dev

# Execution des tests
test:
	uv run pytest

# Verification de la qualite du code
lint:
	uv run ruff check src tests

# Formatage du code
format:
	uv run ruff format src tests

# Nettoyage des fichiers temporaires
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache
