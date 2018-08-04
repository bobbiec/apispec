.PHONY: default
default: help;

develop: venv ## Set up dev environment
	source venv/bin/activate;
	pip install -r dev-requirements.txt;
	pre-commit install --allow-missing-config;

test: venv ## Run all tests in dev environment
	source venv/bin/activate;
	invoke test;

test-all: venv ## Run tests in Python 2.7, 3.5, 3.6 environments
	source venv/bin/activate;
	tox;

docs-develop: venv ## Set up dev environment for Sphinx docs
	pip install -r docs/requirements.txt;

docs: venv ## Build the documentation
	invoke docs -b

venv: ## Create a virtualenv
	virtualenv -p python3 venv

clean: ## Delete the virtualenv
	rm -rf venv

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo 'Make commands (`make $$command`):'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-13s %s\n", $$1, $$2}'
	@echo
	@echo 'Invoke commmands (`invoke $$command`):'
	@invoke -l | tail -n +3
