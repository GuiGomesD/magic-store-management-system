# Wizardry — Magic Store Management System

Sistema de gerenciamento para loja de Magic: The Gathering, usado na disciplina de Métodos de Software.

## Laboratório 2 — Tratamento de erros

Implementado:

- validação de cadastro de usuário com exceções;
- validação de login: obrigatório, máximo 12 caracteres e sem números;
- validação de senha seguindo a política padrão da AWS IAM;
- persistência em RAM;
- persistência em arquivo binário;
- tratamento de erro de persistência;
- tela inicial, tela de login e tela de cadastro;
- diagrama de classes atualizado com fluxo padrão.

## Rotas principais

- `GET /health`
- `GET /usuarios`
- `POST /usuarios`
- `POST /usuarios/login`

## Frontend

Crie `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Depois:

```bash
cd frontend
npm install
npm run dev
```

## Backend com arquivo binário

Windows PowerShell:

```powershell
cd backend
$env:WIZARDRY_PERSISTENCIA="arquivo"
uvicorn app.main:app --reload
```

O arquivo será salvo em `backend/data/usuarios.bin`.
