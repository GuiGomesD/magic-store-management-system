import Link from "next/link";

export default function PaginaInicial() {
  return (
    <main style={{ padding: "2rem", maxWidth: "480px", margin: "0 auto" }}>
      <h1>Magic Store</h1>
      <p>Sistema de gestão da loja Magic.</p>
      <Link href="/admin">Acessar painel admin</Link>
    </main>
  );
}
