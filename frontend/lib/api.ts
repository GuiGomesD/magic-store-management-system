export type Perfil = "cliente" | "gerente";

export type Usuario = {
  id: number;
  nome: string;
  email: string;
  login: string;
  perfil: Perfil;
};

export type Produto = {
  id: number;
  nome: string;
  tipo: string;
  preco: number;
  quantidade_estoque: number;
  gerente_id: number;
};

export type QuantidadeEntidades = {
  quantidade: number;
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

export async function criarGerente(
  nome: string,
  email: string,
  login: string,
  senha: string,
): Promise<Usuario> {
  const resposta = await fetch(`${URL_BASE_API}/usuarios/gerentes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email, login, senha }),
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(resposta, "Não foi possível cadastrar o gerente"),
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

export async function listarProdutos(): Promise<Produto[]> {
  const resposta = await fetch(`${URL_BASE_API}/produtos`);

  if (!resposta.ok) {
    throw new Error("Não foi possível carregar os produtos");
  }

  return resposta.json();
}

export async function criarProduto(dados: {
  nome: string;
  tipo: string;
  preco: number;
  quantidade_estoque: number;
  gerente_id: number;
}): Promise<Produto> {
  const resposta = await fetch(`${URL_BASE_API}/produtos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(resposta, "Não foi possível cadastrar o produto"),
    );
  }

  return resposta.json();
}

export async function removerProduto(id: number): Promise<void> {
  const resposta = await fetch(`${URL_BASE_API}/produtos/${id}`, {
    method: "DELETE",
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(resposta, "Não foi possível remover o produto"),
    );
  }
}

export async function atualizarProduto(
  id: number,
  dados: {
    nome: string;
    tipo: string;
    preco: number;
    quantidade_estoque: number;
  },
): Promise<Produto> {
  const resposta = await fetch(`${URL_BASE_API}/produtos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(
        resposta,
        "Não foi possível atualizar o produto",
      ),
    );
  }

  return resposta.json();
}

export async function desfazerAtualizacaoProduto(id: number): Promise<void> {
  const resposta = await fetch(`${URL_BASE_API}/produtos/${id}/desfazer`, {
    method: "POST",
  });

  if (!resposta.ok) {
    throw new Error(
      await obterMensagemErro(
        resposta,
        "Não foi possível desfazer a atualização do produto",
      ),
    );
  }
}

export async function contarEntidades(): Promise<number> {
  const resposta = await fetch(`${URL_BASE_API}/produtos/quantidade`);

  if (!resposta.ok) {
    throw new Error("Não foi possível carregar a quantidade de entidades");
  }

  const dados: QuantidadeEntidades = await resposta.json();
  return dados.quantidade;
}
