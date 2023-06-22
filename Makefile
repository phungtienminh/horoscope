# Variables
TEST_DIR = tests

# Targets
.PHONY: all test

all: test

test:
	@echo "Running tests..."
	python3 -m unittest discover -s $(TEST_DIR)
	@echo "Done testing."