import csv

ARQUIVO = "../data/banco_eletrico_9770.csv"


def carregar_circuitos(caminho=ARQUIVO):
    circuitos = []
    with open(caminho, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            circuitos.append(row)
    return circuitos


def buscar_por_circuito(cc, circuitos):
    cc = cc.strip().upper()
    return [c for c in circuitos if c["CIRCUITO_CC"].strip().upper() == cc]


def buscar_por_fusivel(fusivel, circuitos):
    fusivel = fusivel.strip().upper()
    return [c for c in circuitos if c["FUSIVEL"].strip().upper() == fusivel]


def buscar_por_componente(nome, circuitos):
    nome = nome.strip().lower()
    return [c for c in circuitos if nome in c["COMPONENTE"].strip().lower()]


if __name__ == "__main__":
    circuitos = carregar_circuitos()

    print("== Circuitos do alternador ==")
    resultados = buscar_por_componente("alternador", circuitos)
    for c in resultados:
        print(
            c["MODELO"],
            c["CIRCUITO_CC"],
            "-",
            c["FUNCAO_DO_CIRCUITO"],
            "| FUSIVEL:",
            c["FUSIVEL"],
        )
