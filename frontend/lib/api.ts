export type Usuario = {
  id: number;
  nome: string;
  email: string;
};

const URL_BASE_API =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

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
): Promise<Usuario> {
  const resposta = await fetch(`${URL_BASE_API}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email }),
  });

  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => null);
    const mensagem =
      corpo?.detail ?? "Não foi possível adicionar o usuário";
    throw new Error(mensagem);
  }

  return resposta.json();
}
