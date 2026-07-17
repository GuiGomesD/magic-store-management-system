"""Gerador mínimo de PDF (texto simples, sem dependências externas).

Monta manualmente os objetos exigidos pelo formato PDF (catálogo, páginas,
conteúdo, fonte) para desenhar linhas de texto em uma ou mais páginas
A4/Carta. Suficiente para relatórios tabulares simples; não implementa
recursos avançados (imagens, quebra automática de linha, etc.).
"""

LARGURA_PAGINA = 612
ALTURA_PAGINA = 792
MARGEM = 72
TAMANHO_FONTE = 11
ALTURA_LINHA = 14
LINHAS_POR_PAGINA = (ALTURA_PAGINA - 2 * MARGEM) // ALTURA_LINHA


def montar_pdf(linhas: list[str]) -> bytes:
    paginas = _paginar(linhas)
    return _serializar_pdf(paginas)


def _paginar(linhas: list[str]) -> list[list[str]]:
    if not linhas:
        return [[]]
    return [
        linhas[indice : indice + LINHAS_POR_PAGINA]
        for indice in range(0, len(linhas), LINHAS_POR_PAGINA)
    ]


def _escapar_texto_pdf(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _montar_stream_texto(linhas: list[str]) -> bytes:
    y_inicial = ALTURA_PAGINA - MARGEM
    partes = ["BT", f"/F1 {TAMANHO_FONTE} Tf", f"{MARGEM} {y_inicial} Td"]
    for indice, linha in enumerate(linhas):
        if indice > 0:
            partes.append(f"0 -{ALTURA_LINHA} Td")
        partes.append(f"({_escapar_texto_pdf(linha)}) Tj")
    partes.append("ET")
    return "\n".join(partes).encode("cp1252", errors="replace")


def _serializar_pdf(paginas: list[list[str]]) -> bytes:
    num_paginas = len(paginas)
    id_catalogo = 1
    id_pages = 2
    ids_paginas = [3 + i for i in range(num_paginas)]
    ids_conteudos = [3 + num_paginas + i for i in range(num_paginas)]
    id_fonte = 3 + 2 * num_paginas

    objetos: dict[int, bytes] = {}

    objetos[id_catalogo] = f"<< /Type /Catalog /Pages {id_pages} 0 R >>".encode("latin-1")

    kids = " ".join(f"{pagina_id} 0 R" for pagina_id in ids_paginas)
    objetos[id_pages] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {num_paginas} >>".encode("latin-1")
    )

    for indice, pagina_id in enumerate(ids_paginas):
        conteudo_id = ids_conteudos[indice]
        objetos[pagina_id] = (
            f"<< /Type /Page /Parent {id_pages} 0 R "
            f"/Resources << /Font << /F1 {id_fonte} 0 R >> >> "
            f"/MediaBox [0 0 {LARGURA_PAGINA} {ALTURA_PAGINA}] "
            f"/Contents {conteudo_id} 0 R >>"
        ).encode("latin-1")

    for indice, linhas_pagina in enumerate(paginas):
        stream = _montar_stream_texto(linhas_pagina)
        objetos[ids_conteudos[indice]] = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
            + stream
            + b"\nendstream"
        )

    objetos[id_fonte] = (
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        b"/Encoding /WinAnsiEncoding >>"
    )

    return _montar_arquivo_pdf(objetos)


def _montar_arquivo_pdf(objetos: dict[int, bytes]) -> bytes:
    saida = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: dict[int, int] = {}

    for id_objeto in sorted(objetos):
        offsets[id_objeto] = len(saida)
        saida += f"{id_objeto} 0 obj\n".encode("latin-1")
        saida += objetos[id_objeto]
        saida += b"\nendobj\n"

    inicio_xref = len(saida)
    total_objetos = max(objetos) + 1
    saida += f"xref\n0 {total_objetos}\n".encode("latin-1")
    saida += b"0000000000 65535 f \n"
    for id_objeto in range(1, total_objetos):
        saida += f"{offsets[id_objeto]:010d} 00000 n \n".encode("latin-1")

    saida += (
        f"trailer\n<< /Size {total_objetos} /Root 1 0 R >>\n"
        f"startxref\n{inicio_xref}\n%%EOF"
    ).encode("latin-1")

    return bytes(saida)
