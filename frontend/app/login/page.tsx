"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { autenticarUsuario } from "@/lib/api";

export default function PaginaLogin() {
  const [login, setLogin] = useState("");
  const [senha, setSenha] = useState("");
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);
  const [mensagemSucesso, setMensagemSucesso] = useState<string | null>(null);

  async function handleSubmit(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setMensagemErro(null);
    setMensagemSucesso(null);

    try {
      const usuario = await autenticarUsuario(login, senha);
      setMensagemSucesso(`Login realizado com sucesso. Bem-vindo(a), ${usuario.nome}.`);
      setLogin("");
      setSenha("");
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao fazer login",
      );
    }
  }

  return (
    <main className="page-shell" style={{ maxWidth: "520px" }}>
      <section className="card">
        <p style={{ margin: 0, color: "#534ab7", fontWeight: 700 }}>Wizardry</p>
        <h1 style={{ marginTop: "0.25rem" }}>Login</h1>
        <p style={{ color: "#555" }}>
          Acesse usando o login e a senha cadastrados no sistema.
        </p>

        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: "0.9rem" }}
        >
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

          <button type="submit">Entrar</button>
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

        <div style={{ marginTop: "1rem", textAlign: "center" }}>
          <Link className="link-button secondary-button" href="/cadastro">
            Criar cadastro
          </Link>
        </div>
      </section>
    </main>
  );
}
