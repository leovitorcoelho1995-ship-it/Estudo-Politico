# Plano de coleta de fontes dos eventos

Objetivo: preencher `data/raw/political_event_sources.csv` com pelo menos uma fonte verificavel por evento antes de publicar o projeto.

## Regra minima

Cada evento precisa de:

- `source_title`: titulo curto da fonte;
- `source_url`: URL verificavel;
- `source_type`: `primary`, `official`, `news`, `database` ou `reference`;
- `source_status`: `verified`;
- `notes`: comentario curto quando houver ambiguidade.

## Fontes preferidas

Prioridade:

1. fontes oficiais;
2. comunicados de banco central, governo, congresso ou organismo internacional;
3. Reuters/AP/BBC/NYT/FT/WSJ/La Nacion/Folha/Valor/G1/Agencia Brasil, conforme pais e evento;
4. Wikipedia apenas como apoio, nao como fonte principal, quando houver fonte melhor.

## Blocos de trabalho

### Bloco 1: eventos top score

Priorizar os eventos que aparecem no topo do `event_final_score.csv`, porque sao os mais visiveis no app.

Primeiro lote recomendado:

1. BRA - Teto do ICMS dos combustiveis
2. USA - CARES Act
3. USA - American Rescue Plan
4. USA - Corte emergencial de juros do Fed
5. USA - Fed leva juros a zero e relanca QE
6. USA - Pandemia Covid
7. USA - Inflation Reduction Act
8. USA - Invasao do Capitolio
9. ARG - Primarias com Milei forte
10. ARG - Eleicao Milei

### Bloco 2: Brasil

Total: 34 eventos.

Fontes-alvo:

- Banco Central do Brasil para Copom/Selic;
- Planalto/Camara/Senado para leis e PECs;
- Petrobras para politica de precos;
- Agencia Brasil, G1, Valor ou Folha para eventos politicos e crises.

### Bloco 3: Estados Unidos

Total: 29 eventos.

Fontes-alvo:

- Federal Reserve para decisoes de juros;
- White House/Congress.gov para leis e pacotes fiscais;
- FDIC/Federal Reserve para SVB/First Republic;
- Reuters/AP/BBC para eventos politicos e eleitorais.

### Bloco 4: Argentina

Total: 25 eventos.

Fontes-alvo:

- Banco Central de la Republica Argentina;
- Ministerio de Economia;
- FMI;
- Casa Rosada;
- Reuters, La Nacion, Ambito, BBC Mundo.

## Como preencher

Editar:

```text
data/raw/political_event_sources.csv
```

Depois rodar:

```powershell
python scripts/build_event_sources_template.py
python scripts/run_pipeline.py --skip-charts
```

## Criterio de pronto

Para publicacao defensavel:

- 88/88 eventos com `source_status = verified`;
- 88/88 eventos com `source_url` iniciado por `https://` ou `http://`;
- top 15 do score com fontes oficiais ou noticias reputaveis.

## Observacao sobre o ranking

O evento `Teto do ICMS dos combustiveis` aparece como #1 no `score_v1_1_trends_partial`.
Tecnicamente isso pode fazer sentido pelo tamanho do movimento em IPCA/gasolina, mas narrativamente e um evento muito brasileiro. Para portfolio, considerar:

- usar ranking por pais como narrativa principal;
- ou abrir com eventos internacionalmente reconheciveis e deixar o score global como ferramenta exploratoria;
- ou criar uma flag editorial `portfolio_anchor` no futuro.
