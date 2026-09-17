# Power BI — Turno a Turno (Produção x Meta)

Relatório de acompanhamento da produção das máquinas da planta de **Itapetininga**,
comparando **Produção Real x Meta**, quebrado por **turno** e organizado pela
hierarquia **Área → Grupo → Máquina**.

Os dados chegam pelo **dataflow da empresa** (tabela `Hora a Hora`), com um registro
por máquina por hora. Este repositório documenta toda a modelagem (colunas, tabela
de dimensão e medidas em DAX) e como montar os visuais.

---

## 1. Estrutura dos arquivos

| Arquivo | O que é |
|---|---|
| `01_colunas_calculadas.dax` | Colunas `Turno` e `Data_Turno` (Nova Coluna na tabela `Hora a Hora`) |
| `03_dim_Maquinas.dax` | Tabela de dimensão das máquinas (Nova Tabela) |
| `04_medidas.dax` | Todas as medidas (Nova Medida) |
| `README.md` | Este guia |

---

## 2. Definição dos turnos

| Turno | Horário (hora de **início**) |
|---|---|
| Turno 1 | 06:00 às 13:59 |
| Turno 2 | 14:00 às 21:59 |
| Turno 3 | 22:00 às 05:59 (vira a noite) |

**Ponto crítico:** a classificação usa `TIMESTAMP_INICIO` (hora de **início** do
período), **não** a coluna `HORA` (que é a hora de **fim**). Usar `HORA` fazia as
horas de fronteira (05h, 13h, 21h) caírem no turno errado — esse era o bug mais
sério do projeto, já corrigido.

### Virada de meia-noite (Turno 3)

A coluna `Data_Turno` joga a **madrugada (00h–05h) para o dia anterior**, porque ela
pertence ao turno que começou na noite anterior. Exemplo:

> **Turno 3 do dia 15/06** = 22h e 23h do dia 15 **+** 00h até 05h do dia 16.
> Todas essas linhas ficam com `Data_Turno = 15/06`.

Ou seja, a madrugada nunca se mistura com o 22h–00h do mesmo dia calendário —
sempre pertence ao turno que iniciou na véspera.

---

## 3. Hierarquia das máquinas (`dim_Maquinas`)

Tabela calculada que mapeia cada máquina para **Área → (Setor) → Grupo → Máquina**.
Relaciona-se com `Hora a Hora[MAQUINA]` (1 → muitos, direção única).

- **Áreas:** PSD, CMSD, SPSD.
- **Setor:** nível extra criado para o guarda-chuva "Respiradores" (que contém os
  grupos SCAF, AURA, CPC3, SELAD_CART, PREFORMER, MKRESIN, FINISHER). Para os
  demais grupos, `Setor = Grupo` (repetido). **Hoje a Matriz usa só Área → Grupo →
  Máquina**; o campo `Setor` existe na tabela mas não é exibido (ficou visualmente
  ruim quando adicionado). Está guardado caso queira usar no futuro.

### Regras de negócio embutidas

- **Grupos somados no DAX** (a soma vem dos filhos): Ear Plug, Injetoras,
  COBRIDEIRAS, CORT, LAM, SCAF, CORDS, FABRIMA13, FABRIMA24.
- **Linhas "pai" ignoradas:** no banco existem linhas `FABRIMA13`, `FABRIMA24` e
  `CORDS` sem sufixo. As de **FABRIMA em unidades** são lixo/duplicata e ficam de
  fora — usamos só os filhos (`FABR13_A..D`, `FABR24_A..D`, `CORDS_A..F`).
- **FABRIMA CX:** as linhas `FABRIMA13` e `FABRIMA24` (sem sufixo) na verdade
  trazem a contagem **em CAIXAS** (escala bem menor, ~17/136/120). Elas formam o
  grupo próprio **FABRIMA CX** dentro de PSD. ⚠️ Escala diferente dos FABRIMA
  A/B/C/D (unidades) — não somar junto.
- **Máquinas de outras plantas / não mapeadas:** ficam com Área em branco e são
  removidas por um **filtro de nível de página** (`Area` não é (Em Branco)).

### Máquinas por área (resumo)

- **PSD:** Ear Plug (MKEAR1–2) · FABRIMA13 (FABR13_A–D) · FABRIMA24 (FABR24_A–D) ·
  FABRIMA CX (FABRIMA13, FABRIMA24 em caixas) · CORDS (CORDS_A–F, REUSA_FLOW) ·
  Injetoras (INJ_01–18, 31, 32) · Respiradores (SCAF1/3/4/5, SELAD_CART, PREFORMER,
  MKRESIN, FINISHER, AURA, CPC3).
- **CMSD:** COBRIDEIRAS (COBR5, COBR8) · CORT (CORT6, FITA10/11/31/32, PCDFITA10) ·
  LAM (LAM1E2, LAM3–8) · IMP4 · EBL · HOOK · LEVELHOOK · NOPP · TRAT_PAPEL.
- **SPSD:** CAPPER · AQUA · GRINDER · PLISSA.

> **Pendente:** `PELETIZA` (Centro_Trabalho 152901, CMSD) apareceu na base mas
> ainda não foi classificada — está fora até confirmar o que é.

---

## 4. Medidas (ver `04_medidas.dax`)

- **Por turno:** `Real T1/T2/T3`, `Meta T1/T2/T3`, `% T1/T2/T3`.
- **Totais:** `Real Total`, `Meta Total`, `% Total`.
- **Genéricas:** `Real`, `Meta Linha`, `%` (sem turno fixo — reagem ao contexto).
- **Gráfico de barras:** `Faltante = MAX(Meta Linha − Real, 0)`.
- **Linhas de média:** `Meta Media`, `Producao Media` (retas no período, com tooltip).
- **Cores:** `Cor T1/T2/T3/Total` (para formatação condicional por "Campo de valor").

As `Meta T1/T2/T3` usam `IF(N IN VALUES(Turno), ...)` para que, na página 2, cada
linha de meta apareça/suma conforme o slicer de Turno (na Matriz continuam normais).

---

## 5. Visuais

### Página 1 — Matriz "Turno a Turno"
- **Linhas:** `Area`, `Grupo`, `Maquina` (de `dim_Maquinas`).
- **Valores:** Real T1/T2/T3, Meta T1/T2/T3, % T1/T2/T3, Real/Meta Total, % Total.
- **Slicer de data:** `Data_Turno`, seleção de **um dia**, ordenado do mais recente
  para o mais antigo.
- **Cores condicionais:** colunas Real/%/Total pintadas por desempenho (verde ≥75%,
  amarelo 50–75%, vermelho <50%), via medidas `Cor Tx` no modo "Campo de valor".
  ⚠️ O `% Total` guarda valor **decimal** (0,63 = 63%); as faixas usam 0 / 0,5 /
  0,75, não 0 / 50 / 75.
- Colunas do T2 destacadas em azul claro.

### Página 2 — Gráfico por período + máquina
- **Slicers:** intervalo de data (De/Até), **uma** máquina, e Turno (1/2/3).
- **Gráfico de colunas empilhadas** (estilo "termômetro"): `Real` (verde) na base +
  `Faltante` (vermelho) em cima — a barra sobe até a Meta, mostrando quanto foi
  feito e quanto faltou. Eixo X = `Data_Turno` + `Turno`.
- Linhas de referência `Meta Media` e `Producao Media` (retas no período).
- **Mini-tabela de ranking por turno:** `Turno` nas linhas + `Real`, `Meta Linha`,
  `%` — resume produção x meta x % do período/máquina selecionados, com linha de
  Total.

---

## 6. Validação

A lógica (Turno, Data_Turno, agrupamentos, Real/Meta) foi conferida contra o dataset
real completo (~122 mil linhas) via reprodução independente em Python — bateu **ao
centavo** para várias máquinas e turnos (ex.: COBR5 Real T1 = 105.279,76).

---

## 7. Erros comuns (e a causa)

| Sintoma | Causa / correção |
|---|---|
| Números gigantes na Matriz | Slicer de data sem dia selecionado, ou linha de Área em branco (máquinas não mapeadas) — filtrar `Area` não vazia. |
| Somas do turno não batem com Excel | Usar `TIMESTAMP_INICIO`, não `HORA`. Turno 3 puxa a madrugada do dia seguinte. |
| Slicer "Grupo, Maquina" com "(Em branco)" | Está filtrando máquinas não mapeadas — desmarcar o "(Em branco)" e/ou filtrar Área não vazia. |
| Cor condicional pinta tudo de vermelho | Faixas em escala 0–100 num valor decimal 0–2 — usar 0 / 0,5 / 0,75; e basear a cor no campo `% Tx`, não no `Real Tx`. |
| Linha de meta some/erra escala | `Meta Media` deve usar `AVERAGEX(SUMMARIZE(...))` + `ALLSELECTED(Data_Turno)`, não `AVERAGE` nem `SUM` direto. |
