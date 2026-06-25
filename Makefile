PYTHON_VERSION ?= 3.13
APP_NAME := claude-code-cli
SAMPLE_DIR := sample_project
PIPX_BIN ?= $(HOME)/.local/bin

.PHONY: help sync lock run run-local run-sample pipx-install pipx-reinstall pipx-uninstall pipx-list ensurepath clean check

help:
	@echo "Available commands:"
	@echo "  make sync            Install/update local uv environment"
	@echo "  make lock            Refresh uv.lock"
	@echo "  make run             Reinstall pipx CLI, then run it from sample_project"
	@echo "  make run-local       Run CLI from repo root with uv"
	@echo "  make run-sample      Run installed CLI from sample_project without reinstalling"
	@echo "  make pipx-install    Install CLI globally with pipx using Python $(PYTHON_VERSION)"
	@echo "  make pipx-reinstall  Reinstall global pipx CLI after code changes"
	@echo "  make pipx-uninstall  Remove global pipx CLI"
	@echo "  make pipx-list       Show pipx installs"
	@echo "  make ensurepath      Add pipx app dir to PATH"
	@echo "  make check           Compile source files"
	@echo "  make clean           Remove Python caches"

sync:
	uv sync

lock:
	uv lock --python $(PYTHON_VERSION)

run: pipx-reinstall run-sample

run-local:
	uv run $(APP_NAME)

run-sample:
	cd $(SAMPLE_DIR) && $(PIPX_BIN)/$(APP_NAME)

pipx-install:
	pipx install . --python $(PYTHON_VERSION)

pipx-reinstall:
	pipx reinstall $(APP_NAME) --python $(PYTHON_VERSION)

pipx-uninstall:
	pipx uninstall $(APP_NAME)

pipx-list:
	pipx list

ensurepath:
	pipx ensurepath

check:
	uv run python -m compileall -q src $(SAMPLE_DIR)

clean:
	find src $(SAMPLE_DIR) -type d -name '__pycache__' -prune -exec rm -rf {} +
