export type Usuario = {
  id: number;
  nome: string;
  email: string;
  login: string;
};

const URL_BASE_API =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function obterMensagemErro(resposta: Response, mensagemPadrao: string) {
  const corpo = await resposta.json().catch(() => null);
  return corpo?.detail ?? mensagemPadrao;
}

export async function listarUsuarios(): Promise<Usuario[]> {
  const resposta = await fetch(`${URL_BASE_API}/usuarios`);

  if (!resposta.ok) {
    throw new Error("Não foi possível carregar os usuários");
  }

  return resposta.json();
}

export async function criarUsuario(
  nome: string,
  email: string,
  login: string,
  senha: string,
): Promise<Usuario> {
  const resposta = await fetch(`${URL_BASE_API}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email, login, senha }),
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(resposta, "Não foi possível adicionar o usuário"),
    );
  }

  return resposta.json();
}

export async function autenticarUsuario(
  login: string,
  senha: string,
): Promise<Usuario> {
  const resposta = await fetch(`${URL_BASE_API}/usuarios/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ login, senha }),
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(resposta, "Não foi possível fazer login"),
    );
  }

  return resposta.json();
}
