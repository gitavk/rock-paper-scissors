build-migration:
	alembic revision --autogenerate -m $(migrate_name)

migrate:
	alembic upgrade head

run:
	uvicorn app.main:app --reload

format:
	poetry run black app
	poetry run isort app

lint:
	poetry run flake8 app
	poetry run mypy app
