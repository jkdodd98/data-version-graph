export PYTHONPATH := $(shell pwd)

.ONESHELL:
.DEFAULT_GOAL := help

POETRY := $(shell command -v poetry 2> /dev/null)

.PHONY: help clean test format lint

#################################################################################
# GLOBAL COMMANDS                                                               #
#################################################################################

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

clean:  ## Remove temporary and generated files
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".*_cache" -exec rm -rf {} +;

test: ## Run tests
	$(POETRY) run coverage run -m pytest tests/**/test_*.py && $(POETRY) run coverage report --show-missing

format: ## Format code using ruff
	$(POETRY) run ruff check --fix data_version_graph

lint:  ## Lint using ruff and mypy
	$(POETRY) run ruff check data_version_graph
	$(POETRY) run mypy --config-file=tox.ini data_version_graph