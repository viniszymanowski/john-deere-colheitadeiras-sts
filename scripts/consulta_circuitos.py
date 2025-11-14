import csv

ARQUIVO = "../data/banco_eletrico_9770.csv"


def carregar_circuitos(caminho=ARQUIVO):
    circuitos = []
    with open(caminho, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            circuitos.append(row)
