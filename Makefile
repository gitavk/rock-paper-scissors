base_cmd = poetry run

build-migration:
	$(base_cmd) alembic revision --autogenerate -m $(migrate_name)

migrate:
	$(base_cmd) alembic upgrade head

run:
	$(base_cmd) uvicorn app.main:app --reload

format:
	$(base_cmd) black app
	$(base_cmd) isort app
	$(base_cmd) black tests
	$(base_cmd) isort tests

lint:
	$(base_cmd) flake8 app
	$(base_cmd) mypy app

tests-unit:
	$(base_cmd) python -m pytest -vv tests/unit

tests-integration:
	$(base_cmd) python -m pytest -vv tests/integration


tests: tests-unit tests-integration

