TEST_DIR ?= test/
BENCHMARK := $(if $(BENCHMARK),$(BENCHMARK),disable)

clean:
	bash -c "find $(MICROSERVICE_PATH) -name "*.pyc" -exec rm -rf {} \;"

pytest:
	poetry run coverage run --source=$(MICROSERVICE_PATH)/src -m pytest --benchmark-$(BENCHMARK) -x -s -vvvv  --ignore vendor $(MICROSERVICE_PATH)/$(TEST_DIR)
	poetry run coverage report --show-missing

lint-check:
	poetry run autoflake $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test --check --recursive --remove-all-unused-imports --remove-unused-variables
	poetry run isort $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test --check-only --diff
	poetry run black $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test --check
	poetry run flake8 $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test

lint-fix:
	poetry run autoflake $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test --in-place --recursive --remove-all-unused-imports --remove-unused-variables
	poetry run autopep8 $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test --in-place --aggressive --aggressive --recursive
	poetry run isort $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test
	poetry run black $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test

lint: lint-fix lint-check

test: export APP_DEFAULT_ENV=test
test: clean lint pytest
