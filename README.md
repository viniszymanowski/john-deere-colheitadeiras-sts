# Base Técnica – Colheitadeiras John Deere Série STS/Série S

Este repositório organiza informações técnicas de manutenção, diagnóstico e elétrica/hidráulica de colheitadeiras John Deere, com foco inicial na **9770 STS** operando na América do Sul.

## Objetivo

- Centralizar informações que normalmente estão espalhadas em:
  - Manuais de Diagnóstico
  - Manuais de Reparo
  - Catálogos de Peças
- Transformar essas informações em:
  - **Bases de dados estruturadas** (CSV/JSON)
  - **Guias de diagnóstico passo a passo**
  - **Scripts de consulta** (Python) para agilizar o trabalho em campo.

## Estrutura

- `data/`
  - **banco_eletrico_9770.csv**  
    Base com circuitos CC, fusíveis, relés, conectores, componentes e função de cada circuito.

- `docs/`
  - **projeto_banco_eletrico.md**  
    Explica o formato das colunas e como alimentar a base elétrica.

- `scripts/`
  - **consulta_circuitos.py**  
    Script simples em Python para consultar a base elétrica por circuito, fusível ou componente.

## Status

- [x] Criada estrutura inicial do projeto
- [x] Criada base elétrica da 9770 STS (modelo + cabeçalho + exemplo)
- [ ] Preencher todos os circuitos da 9770 STS
- [ ] Expandir para outras máquinas (9470, 9570, 9670, Série S)

## Aviso

Os valores críticos (corrente de fusível, número exato de pinos, etc.) devem sempre ser confirmados no **Manual Técnico oficial (TM)** e no **Catálogo de Peças (EPC)** da máquina específica.
