"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";
import {
  contarEntidades,
  criarGerente,
  criarProduto,
  listarProdutos,
  listarUsuarios,
  removerProduto,
  atualizarProduto,
  desfazerAtualizacaoProduto,
  type Produto,
  type Usuario,
} from "@/lib/api";

const TIPOS_PRODUTO = ["carta", "booster", "deck", "acessorio"];

export default function PaginaPainelAdmin() {
  const [gerentes, setGerentes] = useState<Usuario[]>([]);
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [quantidadeEntidades, setQuantidadeEntidades] = useState(0);
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);
  const [mensagemSucesso, setMensagemSucesso] = useState<string | null>(null);

  // formulário de gerente
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [login, setLogin] = useState("");
  const [senha, setSenha] = useState("");

  // formulário de produto
  const [nomeProduto, setNomeProduto] = useState("");
  const [tipoProduto, setTipoProduto] = useState(TIPOS_PRODUTO[0]);
  const [precoProduto, setPrecoProduto] = useState("");
  const [estoqueProduto, setEstoqueProduto] = useState("");
  const [gerenteId, setGerenteId] = useState("");
  const [produtoEditando, setProdutoEditando] = useState<number | null>(null);

  const carregarDados = useCallback(async () => {
    setMensagemErro(null);
    try {
      const [usuarios, listaProdutos, quantidade] = await Promise.all([
        listarUsuarios(),
        listarProdutos(),
        contarEntidades(),
      ]);
      setGerentes(usuarios.filter((usuario) => usuario.perfil === "gerente"));
      setProdutos(listaProdutos);
      setQuantidadeEntidades(quantidade);
      setProdutoEditando((idAtual) => {
        if (
          idAtual !== null &&
          !listaProdutos.some((produto) => produto.id === idAtual)
        ) {
          limparFormularioProduto();
          return null;
        }
        return idAtual;
      });
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao carregar dados",
      );
    }
  }, []);

  useEffect(() => {
    void carregarDados();
  }, [carregarDados]);

  function limparFormularioProduto() {
    setNomeProduto("");
    setTipoProduto(TIPOS_PRODUTO[0]);
    setPrecoProduto("");
    setEstoqueProduto("");
    setGerenteId("");
  }

  async function handleCadastrarGerente(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setMensagemErro(null);
    setMensagemSucesso(null);

    try {
      await criarGerente(nome, email, login, senha);
      setNome("");
      setEmail("");
      setLogin("");
      setSenha("");
      setMensagemSucesso("Gerente cadastrado com sucesso.");
      await carregarDados();
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao cadastrar gerente",
      );
    }
  }

  async function handleCadastrarProduto(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setMensagemErro(null);
    setMensagemSucesso(null);

    try {
      if (produtoEditando !== null) {
        await atualizarProduto(produtoEditando, {
          nome: nomeProduto,
          tipo: tipoProduto,
          preco: Number(precoProduto),
          quantidade_estoque: Number(estoqueProduto),
        });

        setMensagemSucesso("Produto atualizado com sucesso.");
      } else {
        await criarProduto({
          nome: nomeProduto,
          tipo: tipoProduto,
          preco: Number(precoProduto),
          quantidade_estoque: Number(estoqueProduto),
          gerente_id: Number(gerenteId),
        });

        setMensagemSucesso("Produto cadastrado com sucesso.");
      }

      setProdutoEditando(null);
      limparFormularioProduto();

      await carregarDados();
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao cadastrar produto",
      );
    }
  }

  async function handleRemoverProduto(id: number) {
    setMensagemErro(null);
    setMensagemSucesso(null);

    try {
      await removerProduto(id);
      setMensagemSucesso("Produto removido com sucesso.");

      // Se o produto removido era o que estava sendo editado, sai do
      // modo de edição imediatamente (não espera o carregarDados).
      if (produtoEditando === id) {
        setProdutoEditando(null);
        limparFormularioProduto();
      }

      await carregarDados();
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao remover produto",
      );
    }
  }

  function handleEditarProduto(produto: Produto) {
    setMensagemErro(null);
    setMensagemSucesso(null);

    setProdutoEditando(produto.id);

    setNomeProduto(produto.nome);
    setTipoProduto(produto.tipo);
    setPrecoProduto(produto.preco.toString());
    setEstoqueProduto(produto.quantidade_estoque.toString());
    setGerenteId(produto.gerente_id.toString());

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  function handleCancelarEdicao() {
    setProdutoEditando(null);
    limparFormularioProduto();
    setMensagemErro(null);
    setMensagemSucesso(null);
  }

  async function handleDesfazerAtualizacao(id: number) {
    setMensagemErro(null);
    setMensagemSucesso(null);

    try {
      await desfazerAtualizacaoProduto(id);
      setMensagemSucesso("Última atualização desfeita com sucesso.");

      // Se o produto que sofreu "desfazer" é o mesmo que está aberto no
      // formulário de edição, os campos locais ficaram desatualizados
      // em relação ao que voltou no servidor. Sai do modo de edição
      // para evitar sobrescrever o desfazer com dados velhos ao salvar.
      if (produtoEditando === id) {
        setProdutoEditando(null);
        limparFormularioProduto();
      }

      await carregarDados();
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error
          ? erro.message
          : "Erro ao desfazer atualização",
      );
    }
  }

  return (
    <main className="page-shell">
      <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
        <section className="card">
          <p style={{ margin: 0, color: "#534ab7", fontWeight: 700 }}>Wizardry</p>
          <h1 style={{ marginTop: "0.25rem" }}>Painel do gerente</h1>
          <p style={{ color: "#555", marginBottom: 0 }}>
            Entidades cadastradas no sistema:{" "}
            <strong style={{ color: "#534ab7" }}>{quantidadeEntidades}</strong>
          </p>
        </section>

        {mensagemErro && (
          <p role="alert" style={{ color: "#b00020", margin: 0 }}>
            {mensagemErro}
          </p>
        )}
        {mensagemSucesso && (
          <p role="status" style={{ color: "#26734d", margin: 0 }}>
            {mensagemSucesso}
          </p>
        )}

        <section className="card">
          <h2 style={{ marginTop: 0 }}>Cadastrar gerente</h2>
          <form
            onSubmit={handleCadastrarGerente}
            style={{ display: "flex", flexDirection: "column", gap: "0.9rem" }}
          >
            <label>
              Nome
              <input
                className="input-field"
                type="text"
                value={nome}
                onChange={(evento) => setNome(evento.target.value)}
                required
              />
            </label>
            <label>
              E-mail
              <input
                className="input-field"
                type="email"
                value={email}
                onChange={(evento) => setEmail(evento.target.value)}
                required
              />
            </label>
            <label>
              Login
              <input
                className="input-field"
                type="text"
                value={login}
                onChange={(evento) => setLogin(evento.target.value)}
                maxLength={12}
                required
              />
              <small>Máximo 12 caracteres, sem números.</small>
            </label>
            <label>
              Senha
              <input
                className="input-field"
                type="password"
                value={senha}
                onChange={(evento) => setSenha(evento.target.value)}
                required
              />
            </label>
            <button type="submit">Cadastrar gerente</button>
          </form>
        </section>

        <section className="card">
          {gerentes.length === 0 ? (
            <p style={{ color: "#b00020" }}>
              Cadastre um gerente antes de adicionar produtos.
            </p>
          ) : (
            <form
              onSubmit={handleCadastrarProduto}
              style={{ display: "flex", flexDirection: "column", gap: "0.9rem" }}
            >
              <label>
                Nome
                <input
                  className="input-field"
                  type="text"
                  value={nomeProduto}
                  onChange={(evento) => setNomeProduto(evento.target.value)}
                  required
                />
              </label>
              <label>
                Tipo
                <select
                  className="input-field"
                  value={tipoProduto}
                  onChange={(evento) => setTipoProduto(evento.target.value)}
                >
                  {TIPOS_PRODUTO.map((tipo) => (
                    <option key={tipo} value={tipo}>
                      {tipo}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Preço
                <input
                  className="input-field"
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={precoProduto}
                  onChange={(evento) => setPrecoProduto(evento.target.value)}
                  required
                />
              </label>
              <label>
                Quantidade em estoque
                <input
                  className="input-field"
                  type="number"
                  min="0"
                  step="1"
                  value={estoqueProduto}
                  onChange={(evento) => setEstoqueProduto(evento.target.value)}
                  required
                />
              </label>
              <label>
                Gerente responsável
                <select
                  className="input-field"
                  value={gerenteId}
                  onChange={(evento) => setGerenteId(evento.target.value)}
                  required
                  disabled={produtoEditando !== null}
                >
                  <option value="">Selecione um gerente</option>
                  {gerentes.map((gerente) => (
                    <option key={gerente.id} value={gerente.id}>
                      {gerente.nome} (#{gerente.id})
                    </option>
                  ))}
                </select>
                {produtoEditando !== null && (
                  <small>
                    O gerente responsável não é alterado durante a edição.
                  </small>
                )}
              </label>
              <div style={{ display: "flex", gap: "0.75rem" }}>
                <button type="submit">
                  {produtoEditando !== null
                    ? "Salvar alterações"
                    : "Cadastrar produto"}
                </button>
                {produtoEditando !== null && (
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={handleCancelarEdicao}
                  >
                    Cancelar edição
                  </button>
                )}
              </div>
            </form>
          )}
        </section>

        <section className="card">
          <h2 style={{ marginTop: 0 }}>Produtos cadastrados</h2>
          {produtos.length === 0 ? (
            <p>Nenhum produto cadastrado.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  {["ID", "Nome", "Tipo", "Preço", "Estoque", "Gerente", ""].map(
                    (coluna) => (
                      <th
                        key={coluna || "acoes"}
                        style={{
                          textAlign: "left",
                          borderBottom: "1px solid #ccc",
                        }}
                      >
                        {coluna}
                      </th>
                    ),
                  )}
                </tr>
              </thead>
              <tbody>
                {produtos.map((produto) => (
                  <tr
                    key={produto.id}
                    style={
                      produtoEditando === produto.id
                        ? { background: "#f4f2ff" }
                        : undefined
                    }
                  >
                    <td style={{ padding: "0.5rem 0" }}>{produto.id}</td>
                    <td style={{ padding: "0.5rem 0" }}>{produto.nome}</td>
                    <td style={{ padding: "0.5rem 0" }}>{produto.tipo}</td>
                    <td style={{ padding: "0.5rem 0" }}>
                      R$ {produto.preco.toFixed(2)}
                    </td>
                    <td style={{ padding: "0.5rem 0" }}>
                      {produto.quantidade_estoque}
                    </td>
                    <td style={{ padding: "0.5rem 0" }}>#{produto.gerente_id}</td>
                    <td style={{ padding: "0.5rem 0", textAlign: "right" }}>
                      <button
                        type="button"
                        className="secondary-button"
                        style={{ padding: "0.35rem 0.7rem", marginRight: "0.5rem" }}
                        onClick={() => handleEditarProduto(produto)}
                      >
                        Editar
                      </button>

                      <button
                        type="button"
                        className="secondary-button"
                        style={{ padding: "0.35rem 0.7rem", marginRight: "0.5rem" }}
                        onClick={() => handleDesfazerAtualizacao(produto.id)}
                      >
                        Desfazer
                      </button>

                      <button
                        type="button"
                        className="secondary-button"
                        style={{ padding: "0.35rem 0.7rem" }}
                        onClick={() => handleRemoverProduto(produto.id)}
                      >
                        Remover
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <div>
          <Link className="link-button secondary-button" href="/cadastro">
            Voltar para cadastro
          </Link>
        </div>
      </div>
    </main>
  );
}