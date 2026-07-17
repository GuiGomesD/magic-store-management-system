# Magic Store Management System

## Backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

API em `http://localhost:8000`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Painel admin em `http://localhost:3000/admin`.

Variável `NEXT_PUBLIC_API_URL` (padrão: `http://localhost:8000`) em `frontend/.env.local`.
