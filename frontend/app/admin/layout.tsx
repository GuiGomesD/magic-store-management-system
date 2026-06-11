export default function LayoutPainelAdmin({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div style={{ minHeight: "100vh", background: "#fff" }}>
      <header
        style={{
          padding: "1rem 2rem",
          borderBottom: "1px solid #e0e0e0",
          background: "#26215c",
          color: "#fff",
        }}
      >
        <h1 style={{ margin: 0, fontSize: "1.25rem" }}>Painel Admin</h1>
      </header>
      <main style={{ padding: "2rem", maxWidth: "720px", margin: "0 auto" }}>
        {children}
      </main>
    </div>
  );
}
