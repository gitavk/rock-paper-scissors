build-migration:
	alembic revision --autogenerate -m $(migrate_name)

migrate:
	alembic upgrade head

run:
	uvicorn app.main:app --reload

format:
	poetry run black app
	poetry run isort app
	poetry run black tests
	poetry run isort tests

lint:
	poetry run flake8 app
	poetry run mypy app

tests-unit:
	poetry run python -m pytest -vv tests/unit

tests-integration:
	poetry run python -m pytest -vv tests/integration


tests: tests-unit tests-integration

