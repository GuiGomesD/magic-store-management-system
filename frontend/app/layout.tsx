import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Magic Store",
  description: "Sistema de gestão da loja Magic",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
