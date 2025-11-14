import re
import csv
import os
import pdfplumber

# Pasta onde estão seus PDFs
PDF_DIR = os.path.join("..", "Manuals")

# Arquivo final
SAIDA_CSV = os.path.join("..", "data", "codigos_diagnostico.csv")

# Padrão dos códigos
PADRAO_CODIGO = re.compile(r"\b(CAB|LCU|HCC|ATC|RCU|SIV|HCM|ACM)\s+(\d{3,6}\.\d{2})\b")

def extrair_codigos(caminho_pdf):
    print(f"\nLendo: {os.path.basename(caminho_pdf)}")
    registros = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina_num, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if not texto:
                continue
            for linha in texto.split("\n"):
                m = PADRAO_CODIGO.search(linha)
                if m:
                    registros.append({
                        "ARQUIVO": os.path.basename(caminho_pdf),
                        "MODULO": m.group(1),
                        "CODIGO": m.group(2),
                        "DESCRICAO": linha[m.end():].strip(),
                        "PAGINA": pagina_num,
                        "LINHA_BRUTA": linha
                    })

    print(f"  -> {len(registros)} códigos encontrados")
    return registros


print("Procurando PDFs de diagnóstico...\n")

todos = []

# Lê só arquivos com "diagn" no nome — rápido!
for nome in os.listdir(PDF_DIR):
    if nome.lower().endswith(".pdf") and "diagn" in nome.lower():
        caminho = os.path.join(PDF_DIR, nome)
        todos.extend(extrair_codigos(caminho))

# Salva
with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["ARQUIVO", "MODULO", "CODIGO", "DESCRICAO", "PAGINA", "LINHA_BRUTA"])
    writer.writeheader()
    writer.writerows(todos)

print(f"\nTotal final: {len(todos)} códigos")
print(f"Salvo em: {SAIDA_CSV}")
print("\nConcluído.")
