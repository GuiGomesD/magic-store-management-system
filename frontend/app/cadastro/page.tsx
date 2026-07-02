"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";
import { criarUsuario, listarUsuarios, type Usuario } from "@/lib/api";

export default function PaginaCadastro() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [login, setLogin] = useState("");
  const [senha, setSenha] = useState("");
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);
  const [mensagemSucesso, setMensagemSucesso] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(true);

  const carregarUsuarios = useCallback(async () => {
    setCarregando(true);
    setMensagemErro(null);

    try {
      const lista = await listarUsuarios();
      setUsuarios(lista);
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao carregar usuários",
      );
    } finally {
      setCarregando(false);
    }
  }, []);

  useEffect(() => {
    void carregarUsuarios();
  }, [carregarUsuarios]);

  async function handleSubmit(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setMensagemErro(null);
    setMensagemSucesso(null);

    try {
      await criarUsuario(nome, email, login, senha);
      setNome("");
      setEmail("");
      setLogin("");
      setSenha("");
      setMensagemSucesso("Usuário cadastrado com sucesso.");
      await carregarUsuarios();
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao adicionar usuário",
      );
    }
  }

  return (
    <main className="page-shell">
      <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
        <section className="card">
          <p style={{ margin: 0, color: "#534ab7", fontWeight: 700 }}>Wizardry</p>
          <h1 style={{ marginTop: "0.25rem" }}>Cadastro de usuário</h1>
          <p style={{ color: "#555" }}>
            O cadastro valida login, senha e salva os usuários em RAM ou arquivo binário.
          </p>

          <form
            onSubmit={handleSubmit}
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
              <small>
                Mínimo 8 e máximo 128 caracteres, caracteres maiúsculos, minusculos e números ou símbolos.
              </small>
            </label>

            <button type="submit">Cadastrar</button>
          </form>

          {mensagemErro && (
            <p role="alert" style={{ color: "#b00020", marginBottom: 0 }}>
              {mensagemErro}
            </p>
          )}

          {mensagemSucesso && (
            <p role="status" style={{ color: "#26734d", marginBottom: 0 }}>
              {mensagemSucesso}
            </p>
          )}

          <div style={{ marginTop: "1rem", display: "flex", gap: "0.75rem" }}>
            <Link className="link-button secondary-button" href="/login">
              Voltar para login
            </Link>
            <Link className="link-button" href="/admin">
              Painel do gerente
            </Link>
          </div>
        </section>

        <section className="card">
          <h2 style={{ marginTop: 0 }}>Usuários cadastrados</h2>
          {carregando ? (
            <p>Carregando...</p>
          ) : usuarios.length === 0 ? (
            <p>Nenhum usuário cadastrado.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
                    ID
                  </th>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
                    Nome
                  </th>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
                    E-mail
                  </th>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
                    Login
                  </th>
                  <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
                    Perfil
                  </th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((usuario) => (
                  <tr key={usuario.id}>
                    <td style={{ padding: "0.5rem 0" }}>{usuario.id}</td>
                    <td style={{ padding: "0.5rem 0" }}>{usuario.nome}</td>
                    <td style={{ padding: "0.5rem 0" }}>{usuario.email}</td>
                    <td style={{ padding: "0.5rem 0" }}>{usuario.login}</td>
                    <td style={{ padding: "0.5rem 0" }}>
                      {usuario.perfil === "gerente" ? (
                        <span
                          style={{
                            background: "#534ab7",
                            color: "#fff",
                            borderRadius: "999px",
                            fontSize: "0.75rem",
                            fontWeight: 700,
                            padding: "0.15rem 0.6rem",
                          }}
                        >
                          Gerente
                        </span>
                      ) : (
                        <span style={{ color: "#777" }}>Cliente</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </div>
    </main>
  );
}
