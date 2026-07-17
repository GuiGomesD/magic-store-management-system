import Link from "next/link";

export default function PaginaInicial() {
  return (
    <main className="page-shell">
      <section className="card" style={{ textAlign: "center" }}>
        <p style={{ margin: 0, color: "#534ab7", fontWeight: 700 }}>Wizardry</p>
        <h1 style={{ marginBottom: "0.5rem" }}>Magic Store</h1>
        <p style={{ color: "#555", marginBottom: "1.5rem" }}>
          Sistema de gerenciamento para loja de Magic: The Gathering.
        </p>
        <Link className="link-button" href="/login">
          Ir para login
        </Link>
      </section>
    </main>
  );
}
