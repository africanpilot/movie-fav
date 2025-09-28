TEST_DIR ?= test/
BENCHMARK := $(if $(BENCHMARK),$(BENCHMARK),disable)

# Dynamic path variables based on microservice structure
SRC_PATH := $(if $(wildcard $(MICROSERVICE_PATH)/src),$(MICROSERVICE_PATH)/src,$(MICROSERVICE_PATH))
LINT_EXCLUDES := $(if $(wildcard $(MICROSERVICE_PATH)/src),,--exclude=__pycache__,*.pyc,.git,test)
FLAKE8_EXCLUDES := $(if $(wildcard $(MICROSERVICE_PATH)/src),,--exclude=__pycache__,*.pyc,.git,test)

clean:
	bash -c "find $(MICROSERVICE_PATH) -name "*.pyc" -exec rm -rf {} \;"

pytest:
	poetry run coverage run --source=$(SRC_PATH) -m pytest --benchmark-$(BENCHMARK) -x -s -vvvv  --ignore vendor $(MICROSERVICE_PATH)/$(TEST_DIR)
	@if [ "$(CICD_MODE)" != "True" ]; then poetry run coverage report --show-missing; fi

lint-check:
	poetry run autoflake $(SRC_PATH) $(MICROSERVICE_PATH)/test --check --recursive --remove-all-unused-imports --remove-unused-variables $(LINT_EXCLUDES)
	poetry run isort $(SRC_PATH) $(MICROSERVICE_PATH)/test --check-only --diff
	poetry run black $(SRC_PATH) $(MICROSERVICE_PATH)/test --check
	poetry run flake8 $(SRC_PATH) $(MICROSERVICE_PATH)/test $(FLAKE8_EXCLUDES)

lint-fix:
	poetry run autoflake $(SRC_PATH) $(MICROSERVICE_PATH)/test --in-place --recursive --remove-all-unused-imports --remove-unused-variables $(LINT_EXCLUDES)
	poetry run autopep8 $(SRC_PATH) $(MICROSERVICE_PATH)/test --in-place --aggressive --aggressive --recursive
	poetry run isort $(SRC_PATH) $(MICROSERVICE_PATH)/test
	poetry run black $(SRC_PATH) $(MICROSERVICE_PATH)/test

lint: lint-fix lint-check

test: export APP_DEFAULT_ENV=test
test: clean lint pytest
