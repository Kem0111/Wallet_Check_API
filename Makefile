start:
	uvicorn app.app:app --host 0.0.0.0 --reload

test:
	poetry run pytest