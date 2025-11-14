import re
import csv
import os
import pdfplumber
from concurrent.futures import ThreadPoolExecutor

# Pasta dos PDFs
PDF_DIR = os.path.join("..", "Manuals")
SAIDA_CSV = os.path.join("..", "data", "codigos_diagnostico.csv")

# regex dos códigos (rápida e eficiente)
PADRAO_CODIGO = re.compile(r"(CAB|LCU|HCC|ATC|RCU|SIV|HCM|ACM)\s+(\d{3,6}\.\d{2})")

def processar_pagina(pagina, numero, nome_pdf):
    """Processa apenas 1 página (modo turbo)."""
    linhas_validas = []
    texto = pagina.extract_text()
    if not texto:
        return []

    # varredura rápida das linhas
    for linha in texto.split("\n"):
        m = PADRAO_CODIGO.search(linha)
        if m:
            modulo = m.group(1)
            codigo = m.group(2)
            descricao = linha[m.end():].strip()

            linhas_validas.append({
                "ARQUIVO": nome_pdf,
                "MODULO": modulo,
                "CODIGO": codigo,
                "DESCRICAO": descricao,
                "PAGINA": numero,
                "LINHA_BRUTA": linha,
            })
    return linhas_validas


def extrair_codigos_pdf(caminho_pdf):
    nome_pdf = os.path.basename(caminho_pdf)
    print(f"Lendo (TURBO): {nome_pdf}")

    registros = []

    with pdfplumber.open(caminho_pdf) as pdf:
        # multiprocessamento para páginas
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = []

            for i, page in enumerate(pdf.pages, start=1):
                futures.append(
                    pool.submit(processar_pagina, page, i, nome_pdf)
                )

            # juntar resultados
            for f in futures:
                registros.extend(f.result())

    print(f"  -> {len(registros)} códigos encontrados")
    return registros


print("PROCURA TURBO POR PDFs DE DIAGNÓSTICO...\n")

todos = []

# Só lê PDFs com “diagn” no nome → muito mais rápido
for nome in os.listdir(PDF_DIR):
    if nome.lower().endswith(".pdf") and "diagn" in nome.lower():
        caminho = os.path.join(PDF_DIR, nome)
        todos.extend(extrair_codigos_pdf(caminho))

# salvar CSV
with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as f:
    campos = ["ARQUIVO", "MODULO", "CODIGO", "DESCRICAO", "PAGINA", "LINHA_BRUTA"]
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    w.writerows(todos)

print(f"\nTOTAL FINAL: {len(todos)} códigos extraídos")
print(f"Arquivo salvo em: {SAIDA_CSV}")
print("\nConcluído.")
