import csv
import sys

ARQUIVO = "../data/banco_eletrico_9770.csv"


def carregar():
    circuitos = []
    with open(ARQUIVO, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            circuitos.append(row)
    return circuitos


def buscar(circuitos, modo, termo):
    termo = termo.lower()

    resultados = []
    for c in circuitos:
        if modo == "cc" and termo == c["CIRCUITO_CC"].lower():
            resultados.append(c)

        elif modo == "fusivel" and termo == c["FUSIVEL"].lower():
            resultados.append(c)

        elif modo == "componente" and termo in c["COMPONENTE"].lower():
            resultados.append(c)

        elif modo == "texto":
            # busca livre em todas as colunas
            for valor in c.values():
                if termo in str(valor).lower():
                    resultados.append(c)
                    break

    return resultados


def imprimir(resultados):
    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    for c in resultados:
        print("-" * 80)
        print(f"MODELO: {c['MODELO']}")
        print(f"SISTEMA: {c['SISTEMA']}")
        print(f"CIRCUITO CC: {c['CIRCUITO_CC']}")
        print(f"FUSIVEL: {c['FUSIVEL']}")
        print(f"RELE: {c['RELE']}")
        print(f"COMPONENTE: {c['COMPONENTE']}")
        print(f"FUNÇÃO: {c['FUNCAO_DO_CIRCUITO']}")
        print(f"LOCAL FÍSICO: {c['LOCAL_FISICO']}")
        print(f"OBS: {c['OBS']}")
        print("-" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""
Uso:
  py busca.py componente alternador
  py busca.py cc CC007
  py busca.py fusivel F030
  py busca.py texto "terra cabine"
""")
        sys.exit()

    modo = sys.argv[1].lower()
    termo = sys.argv[2]

    circuitos = carregar()
    resultados = buscar(circuitos, modo, termo)
    imprimir(resultados)
