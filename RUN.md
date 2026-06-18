# Backend

## Usando persistência em RAM

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Usando persistência em arquivo binário

Windows PowerShell:

```powershell
cd backend
$env:WIZARDRY_PERSISTENCIA="arquivo"
uvicorn app.main:app --reload
```

Linux/macOS:

```bash
cd backend
export WIZARDRY_PERSISTENCIA=arquivo
uvicorn app.main:app --reload
```

O arquivo binário fica em:

```txt
backend/data/usuarios.bin
```

# Frontend

Crie `frontend/.env.local` com:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Depois rode:

```bash
cd frontend
npm install
npm run dev
```

Fluxo de telas:

```txt
Tela inicial -> Login -> Cadastro
```

# Testes

```bash
cd backend
source .venv/bin/activate
pytest -v
```
