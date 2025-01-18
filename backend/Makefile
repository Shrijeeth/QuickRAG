install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

lint:
	python -m pylint app

auto-lint:
	python -m black --safe app