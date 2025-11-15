import os
import re
import csv
from concurrent.futures import ThreadPoolExecutor

from pdf2image import convert_from_path
import pytesseract

# Pasta dos PDFs de diagnóstico
PDF_DIR = os.path.join("..", "Manuals")

# Arquivo de saída
SAIDA_CSV = os.path.join("..", "data", "codigos_diagnostico_ocr.csv")

# Padrão dos códigos (ex.: CAB 123456.01)
PADRAO_CODIGO = re.compile(r"(CAB|LCU|HCC|ATC|RCU|SIV|HCM|ACM)\s+(\d{3,6}\.\d{2})")


def ocr_pagina(img, num_pagina, nome_pdf):
    """Roda OCR em 1 página e devolve códigos encontrados."""
    texto = pytesseract.image_to_string(img)  # OCR
    registros = []

    for linha in texto.split("\n"):
        m = PADRAO_CODIGO.search(linha)
        if m:
            registros.append({
                "ARQUIVO": nome_pdf,
                "MODULO": m.group(1),
                "CODIGO": m.group(2),
                "DESCRICAO": linha[m.end():].strip(),
                "PAGINA": num_pagina,
                "LINHA_BRUTA": linha,
            })

    return registros


def processar_pdf(pdf_path):
    nome_pdf = os.path.basename(pdf_path)
    print(f"\nOCR TURBO: {nome_pdf}")

    # converte todas as páginas para imagem (usa Poppler)
    imagens = convert_from_path(pdf_path, dpi=200)
    registros = []

    # OCR em paralelo nas páginas
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = []
        for i, img in enumerate(imagens, start=1):
            futures.append(pool.submit(ocr_pagina, img, i, nome_pdf))

        for f in futures:
            registros.extend(f.result())

    print(f"  -> {len(registros)} códigos encontrados")
    return registros


if __name__ == "__main__":
    todos = []

    print("OCR TURBO EXTREMO em PDFs de diagnóstico...\n")

    # só pega PDFs com "diagn" no nome
    for nome in os.listdir(PDF_DIR):
        if nome.lower().endswith(".pdf") and "diagn" in nome.lower():
            caminho_pdf = os.path.join(PDF_DIR, nome)
            todos.extend(processar_pdf(caminho_pdf))

    # salva CSV
    campos = ["ARQUIVO", "MODULO", "CODIGO", "DESCRICAO", "PAGINA", "LINHA_BRUTA"]
    os.makedirs(os.path.dirname(SAIDA_CSV), exist_ok=True)
    with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(todos)

    print(f"\nTOTAL FINAL: {len(todos)} códigos")
    print(f"CSV salvo em: {SAIDA_CSV}")
    print("Concluído.")
