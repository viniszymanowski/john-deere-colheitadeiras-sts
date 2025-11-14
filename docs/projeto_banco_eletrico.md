# Projeto – Banco Elétrico 9770 STS

Este documento define o padrão da base de dados elétrica para a colheitadeira **John Deere 9770 STS**.

## Objetivo

Organizar em formato de planilha (CSV) as principais informações dos circuitos elétricos, focando em:

- Circuitos CC
- Fusíveis
- Relés
- Conectores (origem e destino)
- Componentes finais (alternador, motores, sensores, módulos)
- Função do circuito
- Localização física na máquina

## Formato do arquivo `data/banco_eletrico_9770.csv`

Colunas:

1. `MODELO` – Ex.: `9770 STS`
2. `SISTEMA` – Ex.: `Elétrico – Carga`, `Elétrico – Iluminação`
3. `CIRCUITO_CC` – Código do circuito. Ex.: `CC007`
4. `FUSIVEL` – Ex.: `F0xx` (ou `VER_TM` se for dado a confirmar)
5. `RELE` – Ex.: `R0xx` (ou `-` se não houver)
6. `MODULO_ORIGEM` – Ex.: `CAB`, `LCU`, `Chave Ignição`
7. `CONECTOR_ORIGEM` – Ex.: `X123`
8. `PINO_ORIGEM` – Ex.: `Pino 3`
9. `CONECTOR_DESTINO` – Ex.: `Xalt`, `Motor peneira`
10. `PINO_DESTINO` – Ex.: `D+`, `Pino A`
11. `COMPONENTE` – Componente físico final. Ex.: `Alternador`, `Motor do ventilador`
12. `FUNCAO_DO_CIRCUITO` – Descrição em texto. Ex.: `Fornecer 12 V pós-chave para excitar o alternador`
13. `LOCAL_FISICO` – Onde encontrar o componente/trecho principal. Ex.: `Compartimento do motor, lado direito`
14. `OBS` – Observações gerais. Ex.: `Confirmar fusível no TM`, `Ponto crítico de quebra de fio`

## Exemplo de linha (conceito)

```csv
9770 STS,Elétrico – Carga,CC007,VER_TM,VER_TM,Chave Ignição,VER_DIAGRAMA,VER_DIAGRAMA,Conector alternador,D+/EXC,Alternador,Fornecer 12 V pós-chave para excitar o alternador na partida,Compartimento do motor, lado direito,Confirmar número do fusível, relé, conector e pino no manual de circuito elétrico.
