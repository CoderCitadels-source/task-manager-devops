PYTHON:=python
VENV_DIR:=.venv
ACTIVATE:=$(VENV_DIR)\Scripts\activate

.PHONY: install run test docker-build docker-up

install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)\Scripts\pip install -r requirements.txt

run:
	$(VENV_DIR)\Scripts\uvicorn app.main:app --reload --port 8000

test:
	$(VENV_DIR)\Scripts\pytest -q

docker-build:
	docker build -t task-manager-devops:latest .

docker-up:
	docker-compose up --build -d
