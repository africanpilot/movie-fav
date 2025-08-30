TEST_DIR ?= test/
BENCHMARK := $(if $(BENCHMARK),$(BENCHMARK),disable)

clean:
	bash -c "find $(MICROSERVICE_PATH) -name "*.pyc" -exec rm -rf {} \;"

pytest:
	poetry run coverage run -m pytest --benchmark-$(BENCHMARK) -x -s -vvvv  --ignore vendor $(MICROSERVICE_PATH)/$(TEST_DIR)

lint:
	poetry run black $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test --check
	poetry run flake8 $(MICROSERVICE_PATH)/src $(MICROSERVICE_PATH)/test

test: export APP_DEFAULT_ENV=test
test: clean pytest
