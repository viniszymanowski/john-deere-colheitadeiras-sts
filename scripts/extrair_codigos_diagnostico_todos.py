import os
import re
import csv
import shutil
import tempfile
from pdf2image import convert_from_path
import pytesseract

# Caminho do Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Pasta onde estão seus PDFs
PDF_DIR = os.path.join("..", "Manuais Técnicos John Deere")

# Arquivo final
SAIDA_CSV = os.path.join("..", "data", "codigos_diagnostico.csv")

# Regex para localizar códigos (ajuste se necessário)
PADRAO = re.compile(r"\b(CAB|LCU|HCC|ATC|RCU|HCM|SIV|ACM)\s+(\d{3,6}\.\d{2})\b")

def processar_pdf(caminho_pdf):
    print(f"\nLENDO (TURBO): {os.path.basename(caminho_pdf)}")
    registros = []

    # Cria pasta temporária para imagens
    temp_dir = tempfile.mkdtemp()

    # Converte PDF → imagens
    try:
        paginas = convert_from_path(caminho_pdf, dpi=300, output_folder=temp_dir)
    except Exception as e:
        print(f"Erro ao converter PDF: {e}")
        return []

    # OCR de cada página
    for idx, img in enumerate(paginas, start=1):
        texto = pytesseract.image_to_string(img, lang="por+eng")
        for linha in texto.split("\n"):
            m = PADRAO.search(linha)
            if m:
                registro = {
                    "ARQUIVO": os.path.basename(caminho_pdf),
                    "PAGINA": idx,
                    "MODULO": m.group(1),
                    "CODIGO": m.group(2),
                    "LINHA_BRUTA": linha.strip()
                }
                registros.append(registro)

    shutil.rmtree(temp_dir)
    print(f"  -> {len(registros)} códigos encontrados")
    return registros


if __name__ == "__main__":
    todos = []

    print("PROCURANDO PDFs DE DIAGNÓSTICO...\n")

    for nome in os.listdir(PDF_DIR):
        if not nome.lower().endswith(".pdf"):
            continue

        if "diagn" not in nome.lower():
            continue  # só técnicos

        caminho = os.path.join(PDF_DIR, nome)
        todos.extend(processar_pdf(caminho))

    # Salva CSV
    campos = ["ARQUIVO", "PAGINA", "MODULO", "CODIGO", "LINHA_BRUTA"]
    with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for r in todos:
            w.writerow(r)

    print(f"\nTOTAL FINAL DE CÓDIGOS: {len(todos)}")
    print(f"CSV SALVO EM: {SAIDA_CSV}")
    print("\nCONCLUÍDO.")
