import re
import csv
import os

import pdfplumber  # vamos instalar no PC com:  pip install pdfplumber

# Pasta onde estão os PDFs (nome exatamente como está no repositório)
PDF_DIR = os.path.join("..", "Manuais Técnicos John Deere")

# Mapeamento dos PDFs para séries/modelos
# Por enquanto, só Série 70 STS. Depois ampliamos.
FONTES = [
    {
        "serie": "STS70",
        "modelos": ["9470 STS", "9570 STS", "9670 STS", "9770 STS"],
        "pdf": os.path.join(PDF_DIR, "sts70_diagnostico.pdf"),
    },
    # Quando tiver outros PDFs, é só descomentar e ajustar os nomes:
    # {
    #     "serie": "S600",
    #     "modelos": ["S540", "S550", "S660", "S670", "S680", "S690"],
    #     "pdf": os.path.join(PDF_DIR, "s600_diagnostico.pdf"),
    # },
    # {
    #     "serie": "S700",
    #     "modelos": ["S760", "S770", "S780"],
    #     "pdf": os.path.join(PDF_DIR, "s700_diagnostico.pdf"),
    # },
]

SAIDA_CSV = os.path.join("..", "data", "codigos_diagnostico.csv")

# Padrão de código (ajustar depois se o manual tiver outro formato)
# Ex.: CAB 123456.01 / LCU 000123.02 / HCC 456789.00...
PADRAO_CODIGO = re.compile(r"\b(CAB|LCU|HCC|ATC|RCU|SIV|HCM|ACM)\s+(\d{3,6}\.\d{2})\b")


def extrair_linhas_pdf(caminho_pdf):
    linhas = []
    if not os.path.exists(caminho_pdf):
        print(f"[AVISO] PDF não encontrado: {caminho_pdf}")
        return linhas

    with pdfplumber.open(caminho_pdf) as pdf:
        for idx, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if not texto:
                continue
            for linha in texto.split("\n"):
                linhas.append((idx, linha))
    return linhas


def extrair_codigos_de_pdf(serie, modelos, caminho_pdf):
    print(f"\nLendo PDF: {caminho_pdf}")
    linhas = extrair_linhas_pdf(caminho_pdf)
    registros = []

    for pagina, linha in linhas:
        m = PADRAO_CODIGO.search(linha)
        if not m:
            continue

        modulo = m.group(1)
        codigo = m.group(2)
        descricao = linha[m.end():].strip()

        for modelo in modelos:
            registros.append(
                {
                    "SERIE": serie,
                    "MODELO": modelo,
                    "MODULO": modulo,
                    "CODIGO": codigo,
                    "DESCRICAO": descricao,
                    "ORIGEM_PDF": os.path.basename(caminho_pdf),
                    "PAGINA": pagina,
                    "LINHA_BRUTA": linha,
                }
            )

    print(f"  -> {len(registros)} códigos encontrados nesse PDF.")
    return registros


def salvar_todos(registros, caminho_csv):
    campos = ["SERIE", "MODELO", "MODULO", "CODIGO", "DESCRICAO", "ORIGEM_PDF", "PAGINA", "LINHA_BRUTA"]
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in registros:
            writer.writerow(r)


if __name__ == "__main__":
    todos_registros = []

    for fonte in FONTES:
        serie = fonte["serie"]
        modelos = fonte["modelos"]
        pdf = fonte["pdf"]

        registros = extrair_codigos_de_pdf(serie, modelos, pdf)
        todos_registros.extend(registros)

    print(f"\nTotal geral de registros: {len(todos_registros)}")
    print(f"Salvando em {SAIDA_CSV} ...")
    salvar_todos(todos_registros, SAIDA_CSV)
    print("Concluído.")
