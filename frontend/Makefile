# Makefile to configure grc for colorized logs and run the log viewer
# Run: `make log`

SHELL := /bin/bash

# Log file
LOG_FILE = dev.log

# Check if grc is installed
check-grc:
	@if ! command -v grc &> /dev/null; then \
		echo "🔴 grc not found. Installing..."; \
		sudo apt install grc -y || brew install grc; \
	else \
		echo "✅ grc is already installed."; \
	fi

# Check if bat is installed
check-bat:
	@if ! command -v bat &> /dev/null; then \
		echo "🔴 bat not found. Installing..."; \
		sudo apt install bat -y || brew install bat; \
	else \
		echo "✅ bat is already installed."; \
	fi

# View logs with color highlighting
log: check-grc check-bat
	@echo "🚀 Starting log viewer..."
	@grc tail -f $(LOG_FILE) | bat --language=log --paging=never
