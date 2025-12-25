# canteen-api

## Run Postgres
docker compose up -d

## Create virtualenv & install
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

## Run API
uvicorn app.main:app --reload