.PHONY: install run test

install:
	python3 -m pip install -r requirements.txt

run:
	python3 -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

test:
	python3 -m pytest -q
