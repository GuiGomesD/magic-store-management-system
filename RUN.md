# Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

# Frontend

```bash
cd frontend
npm install
npm run dev
```

# Testes

```bash
cd backend
source .venv/bin/activate
pytest -v
```
