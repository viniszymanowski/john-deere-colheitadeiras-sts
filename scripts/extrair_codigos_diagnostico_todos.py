import re
import csv
import os
import pdfplumber

PDF_DIR = os.path.join("..", "Manuais Técnicos John Deere")  # pasta dos PDFs
SAIDA_CSV = os.path.join("..", "data", "codigos_diagnostico.csv")

# regex de códigos
PADRAO_CODIGO = re.compile(r"\b(CAB|LCU|HCC|ATC|RCU|SIV|HCM|ACM)\s+(\d{3,6}\.\d{2})\b")

def extrair_linhas_pdf(caminho_pdf):
    linhas = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for idx, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if not texto:
                continue
            for linha in texto.split("\n"):
                linhas.append((idx, linha))
    return linhas

def extrair_codigos(caminho_pdf):
    print(f"\nLendo: {os.path.basename(caminho_pdf)}")
    linhas = extrair_linhas_pdf(caminho_pdf)
    registros = []

    for pagina, linha in linhas:
        m = PADRAO_CODIGO.search(linha)
        if not m:
            continue

        modulo = m.group(1)
        codigo = m.group(2)
        descricao = linha[m.end():].strip()

        registros.append({
            "ARQUIVO": os.path.basename(caminho_pdf),
            "MODULO": modulo,
            "CODIGO": codigo,
            "DESCRICAO": descricao,
            "PAGINA": pagina,
            "LINHA_BRUTA": linha,
        })

    print(f"  -> {len(registros)} códigos encontrados")
    return registros


if __name__ == "__main__":
    todos = []

    print("Varredura automática de PDF...\n")

    # percorre todos os arquivos da pasta
    for nome in os.listdir(PDF_DIR):
        if nome.lower().endswith(".pdf"):
            caminho = os.path.join(PDF_DIR, nome)
            try:
                registros = extrair_codigos(caminho)
                todos.extend(registros)
            except Exception as e:
                print(f"Erro ao ler {nome}: {e}")

    # salvar CSV
    campos = ["ARQUIVO", "MODULO", "CODIGO", "DESCRICAO", "PAGINA", "LINHA_BRUTA"]
    with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in todos:
            writer.writerow(r)

    print(f"\nTotal final de códigos extraídos: {len(todos)}")
    print(f"CSV salvo em: {SAIDA_CSV}")
    print("\nConcluído.")
