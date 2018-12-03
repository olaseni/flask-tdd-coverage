#
TEST_PATH=tests/

clean-pyc:
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '*~' -delete

clean-cache:
	@[[ -d '.pytest_cache' ]] && rm -rf .pytest_cache &> /dev/null || true

clean-html:
	@[[ -d 'htmlcov' ]] && rm -rf htmlcov &> /dev/null || true

clean: clean-cache clean-pyc clean-html

run-tests:
	coverage run --source application --branch -m pytest -s ${TEST_PATH}

report:
	coverage report -m

html:
	coverage html

tests: clean-pyc run-tests clean-cache

test: tests

init-db:
	python -m flask init-db

run:
	python -m flask run