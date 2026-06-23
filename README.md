# Task Manager — DevOps-focused Demo

This repository contains a minimal FastAPI-based task manager with a DevOps-focused setup: Dockerfile, docker-compose, Makefile, and GitHub Actions CI.

Quick start (Linux/Windows with WSL or PowerShell):

```bash
# create and activate virtualenv
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt

# run locally
uvicorn app.main:app --reload --port 8000
```

Make targets:

```bash
make install    # install dependencies
make run        # run locally
make test       # run tests
make docker-up  # build and run via docker-compose
```

CI: GitHub Actions workflow runs tests on push and PR.
