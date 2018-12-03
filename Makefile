#
TEST_PATH=tests/

clean-pyc:
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '*~' -delete

clean-cache:
	@[[ -d '.pytest_cache' ]] && rm -rf .pytest_cache &> /dev/null

run-tests:
	pytest -s ${TEST_PATH}

tests: clean-pyc run-tests clean-cache

test: tests


init-db:
	flask init-db

run:
	flask run