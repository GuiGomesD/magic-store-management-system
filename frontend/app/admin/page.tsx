"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { criarUsuario, listarUsuarios, type Usuario } from "@/lib/api";

export default function PaginaPainelAdmin() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);
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

    try {
      await criarUsuario(nome, email);
      setNome("");
      setEmail("");
      await carregarUsuarios();
    } catch (erro) {
      setMensagemErro(
        erro instanceof Error ? erro.message : "Erro ao adicionar usuário",
      );
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <section>
        <h2>Adicionar usuário</h2>
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}
        >
          <label>
            Nome
            <input
              type="text"
              value={nome}
              onChange={(evento) => setNome(evento.target.value)}
              required
              style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
            />
          </label>
          <label>
            E-mail
            <input
              type="email"
              value={email}
              onChange={(evento) => setEmail(evento.target.value)}
              required
              style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
            />
          </label>
          <button type="submit">Adicionar</button>
        </form>
      </section>

      {mensagemErro && (
        <p role="alert" style={{ color: "#b00020", margin: 0 }}>
          {mensagemErro}
        </p>
      )}

      <section>
        <h2>Usuários cadastrados</h2>
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
              </tr>
            </thead>
            <tbody>
              {usuarios.map((usuario) => (
                <tr key={usuario.id}>
                  <td style={{ padding: "0.5rem 0" }}>{usuario.id}</td>
                  <td style={{ padding: "0.5rem 0" }}>{usuario.nome}</td>
                  <td style={{ padding: "0.5rem 0" }}>{usuario.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
