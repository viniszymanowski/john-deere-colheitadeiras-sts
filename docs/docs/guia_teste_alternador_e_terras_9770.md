# Guia de Teste – Alternador e Terras Principais – John Deere 9770 STS

Este guia complementa a base `data/banco_eletrico_9770.csv`, com foco nos circuitos:

- `CC007` – Excitação do alternador  
- `ALIM_ALT_BPLUS` – Cabo principal de carga (B+)  
- `ALT_SENSE` – Linha de sense (se houver)  
- `TERRA_ALT` – Terra do alternador  
- `TERRA_MOTOR_CHASSI` – Terra motor ↔ chassi  
- `TERRA_CABINE` – Terra da cabine / módulos eletrônicos  

> ⚠️ **ATENÇÃO – SEGURANÇA**
>
> - Antes de mexer em qualquer chicote: desligar o motor, retirar a chave e aguardar parada completa de todas as partes móveis.  
> - Ao medir com o motor ligado, manter roupas, mãos e ferramentas longe de correias, polias e ventoinhas.  
> - Nunca fazer “jump” de fios sem ter certeza do que está pulando.

---

## 1. Ferramentas necessárias

- Multímetro digital (medir **tensão DC** e, se possível, **queda de tensão mV**).  
- Alicate amperímetro (opcional, para ver corrente de carga).  
- Cabos de teste auxiliares (fio com garras jacaré ajuda bastante).  
- Escova de aço / lixa fina para limpar pontos de terra, se necessário.

---

## 2. Visão geral do sistema de carga

- O alternador da 9770 STS recebe:
  - **B+ (ALIM_ALT_BPLUS):** cabo grosso que leva a corrente de carga até a barra positiva/baterias.
  - **Excitação (CC007):** 12 V pós-chave no terminal **D+ / EXC**, para “acordar” o alternador.
  - **Sense (ALT_SENSE):** em alguns modelos, um fio separado que leva a tensão de referência da bateria ao regulador interno.
  - **Terra (TERRA_ALT):** via carcaça, conectada ao **bloco do motor**.
- O bloco do motor é ligado ao **chassi** pela `TERRA_MOTOR_CHASSI`.
- A cabine e os módulos eletrônicos (CAB, LCU, HCC etc.) usam o `TERRA_CABINE` como referência.

---

## 3. Teste 1 – Estado das baterias e carga básica

1. Com **tudo desligado** há pelo menos alguns minutos:
   - Meça a tensão nos bornes da bateria principal.
   - Valor típico saudável: **~12,4 V a 12,7 V** (bateria em bom estado).
2. Dê a partida e deixe em **marcha lenta**:
   - Meça novamente a tensão nos bornes da bateria.
   - Valor esperado (geral): **entre 13,8 V e 14,5 V**.
3. Acelere para rotação de trabalho:
   - A tensão deve permanecer estável na mesma faixa (sem subir demais nem cair para 12 V).

> Se a tensão fica em **~12 V na lenta** e só sobe quando acelera bem, o alternador geralmente está bom mecanicamente, mas **pode estar sem excitação adequada (CC007)** ou com problema de terra/alimentação.

---

## 4. Teste 2 – Cabo de carga B+ (`ALIM_ALT_BPLUS`)

Objetivo: confirmar que o cabo B+ não tem queda de tensão exagerada entre alternador e bateria.

1. Com o motor em **rotação de trabalho** e algumas cargas ligadas (faróis, ar, etc.):
2. Coloque o multímetro em **escala de tensão DC**.
3. Ponta **vermelha** no terminal **B+ do alternador**.  
4. Ponta **preta** no **borne positivo da bateria**.
5. Leia a queda de tensão.

- Ideal: **≤ 0,3 V** de diferença.  
- Se der algo como **0,5 V, 1 V ou mais**, há:
  - mau contato em terminais,
  - cabo oxidado/rompido internamente,
  - conexão solta em barra de distribuição.

> Esse trecho corresponde ao circuito `ALIM_ALT_BPLUS` na base elétrica.

---

## 5. Teste 3 – Terra do alternador e terra motor ↔ chassi (`TERRA_ALT`, `TERRA_MOTOR_CHASSI`)

### 5.1. Queda de tensão no terra do alternador

1. Motor em rotação de trabalho, com carga elétrica ligada.  
2. Multímetro em **tensão DC**.  
3. Ponta **vermelha** no **borne negativo da bateria**.  
4. Ponta **preta** na **carcaça do alternador** (para furo de fixação ou corpo metálico limpo).  
5. Leia a queda de tensão.

- Ideal: **≤ 0,2 V**.  
- Valores mais altos indicam:
  - oxidação entre alternador e suporte,
  - pintura demais na base de fixação,
  - folga em parafusos,
  - problema na ligação `TERRA_MOTOR_CHASSI`.

### 5.2. Verificar ponte de terra motor ↔ chassi

- Localize o cabo/chapa de terra que liga o **bloco do motor** ao **chassi**.
- Visual:
  - procurar ferrugem, fio verde, isolamento ressecado, terminal “meio solto”.
- Se suspeito, repetir o teste de queda de tensão:
  - Vermelho no **negativo da bateria**,  
  - Preto em um ponto limpo do **bloco do motor**.
  - Se a queda for baixa e boa no bloco, mas ruim no alternador, o problema está na montagem do alternador (`TERRA_ALT`).

---

## 6. Teste 4 – Excitação do alternador (`CC007` – terminal D+ / EXC)

Esse é o teste-chave para o sintoma “**alternador não carrega na lenta, só quando acelera muito**”.

### 6.1. Medir tensão no D+ com chave ligada, motor parado

1. Desconecte o conector pequeno do terminal **D+ / EXC** do alternador (quando possível).  
2. Coloque o multímetro em **tensão DC**.  
3. Ponta **preta** na carcaça do alternador (ou bloco do motor).  
4. Ponta **vermelha** no fio que vai no terminal **D+ / EXC**.  
5. Dê **ignição (chave ligada)**, mas não dê partida.

- Esperado: algo próximo à **tensão da bateria (~12 V)**.  
- Se houver **0 V** ou tensão muito baixa:
  - problema no circuito `CC007`:
    - fusível queimado (`FUSIVEL` = `VER_TM` na base; ver qual é no TM),
    - mau contato em conector entre cabine e motor,
    - fio partido no chicote.

### 6.2. Medir com motor em marcha lenta

1. Ligue o conector novamente no D+.  
2. Com o motor funcionando em **marcha lenta**, repita a medição entre D+ e carcaça.

- Deve haver tensão semelhante à da bateria.  
- Se a tensão só aparece ou sobe corretamente quando acelera muito, o CC007 pode estar “fraco” (por mau contato, resistência alta, etc.).

---

## 7. Teste 5 – Linha de sense (`ALT_SENSE`) – se aplicável

Alguns alternadores usam um terminal de **sense (S)** separado:

1. Identifique no alternador se existe um terminal marcado como **S** ou **Sense**.
2. Com o motor ligado:
   - meça a tensão entre esse terminal e a **carcaça do alternador**.
3. Compare com a tensão diretamente na bateria.

- Diferença grande indica fio danificado ou mau contato no circuito `ALT_SENSE`.
- Sense com leitura errada pode fazer o regulador:
  - carregar demais (tensão alta),
  - ou carregar de menos (tensão baixa).

---

## 8. Teste 6 – Terra da cabine (`TERRA_CABINE`)

Esse teste é importante quando existem:

- mensagens estranhas no monitor,
- falhas intermitentes,
- leituras do sistema elétrico “malucas” quando liga/ar/desliga cargas.

### 8.1. Localizar o ponto de terra

- Consultar o desenho de terra da cabine no manual elétrico.
- Normalmente é um parafuso com vários terminais de fio preto ou marrom, fixo na estrutura da cabine, ligado ao chassi.

### 8.2. Medir queda de tensão

1. Motor em rotação de trabalho, com algumas cargas elétricas ligadas.  
2. Multímetro em **tensão DC**.  
3. Ponta **vermelha** no **negativo da bateria**.  
4. Ponta **preta** diretamente no **ponto de terra da cabine** (parafuso de terra).  

- Ideal: **≤ 0,2 V**.  
- Se for maior:
  - limpar bem o ponto de contato (lixa/escova),
  - reapertar,
  - conferir se não há fios quebrados perto dos terminais.

---

## 9. Resumo de diagnóstico rápido (ligando com o banco elétrico)

- **Bateria OK, B+ OK, terras bons, mas sem 12 V no D+ (CC007):**  
  → Ver circuito de excitação (`CC007`) no `banco_eletrico_9770.csv`: fusível, conector de cabine, chicote até o motor.

- **D+ com 12 V, mas queda grande entre carcaça do alternador e negativo da bateria:**  
  → Ver `TERRA_ALT` e `TERRA_MOTOR_CHASSI`: limpeza de fixações, cabo/chapa de terra, aperto.

- **Carga irregular, tensão louca quando liga coisas da cabine, mensagens aleatórias:**  
  → Ver `TERRA_CABINE`: ponto de terra da cabine e conexões dos módulos (CAB, LCU, HCC).

- **Tensão muito alta ou muito baixa sem motivo aparente e alternador com terminal S:**  
  → Ver `ALT_SENSE`: conferir continuidade e contato até o ponto onde “enxerga” a tensão da bateria.

---

Este guia pode ser impresso ou convertido em PDF para uso em campo, e deve ser sempre usado em conjunto com:

- O **Manual Técnico (TM)** da 9770 STS;  
- O **esquema elétrico oficial**, para confirmação de fusíveis, pinos e conectores.
