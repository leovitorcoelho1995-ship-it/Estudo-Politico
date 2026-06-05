# Relatorio atual do projeto

Data: 2026-06-04

## 1. Resumo executivo

O projeto esta em estado defensavel como aplicacao analitica exploratoria. Ele combina eventos politico-economicos de Brasil, Estados Unidos e Argentina com indicadores economicos, Google Trends parcial, rankings, score sintetico, auditorias e app Streamlit.

O ponto forte central e metodologico: o estudo nao compara economias por valores brutos. Ele compara desvios em relacao ao padrao historico de cada pais e indicador. Isso permite colocar cambio, inflacao, juros, combustiveis, desemprego e PIB em uma unidade comum de leitura.

O limite central tambem esta claro: o estudo mede associacao temporal, nao causalidade formal. Eventos proximos, choques externos, tendencias macro e mudancas de regime podem compartilhar a mesma janela de impacto.

## 2. Estado atual

### Cobertura de eventos

| Pais | Eventos totais | Eventos curto prazo | Eventos anuais | Leitura principal |
| --- | ---: | ---: | ---: | --- |
| Argentina | 25 | 20 | 25 | forte em cambio oficial/blue; limitado em outros indicadores frequentes |
| Brasil | 34 | 32 | 34 | boa cobertura macro: cambio, Selic, IPCA e gasolina |
| Estados Unidos | 29 | 27 | 29 | boa cobertura FRED, mas com frequencias mistas |
| Projeto | 88 | 79 | 88 | volume suficiente para exploracao por pais e categoria |

### Google Trends

| Pais | Coletados | Pendentes coleta | Sem termos-semente |
| --- | ---: | ---: | ---: |
| Argentina | 10 | 10 | 5 |
| Brasil | 8 | 23 | 3 |
| Estados Unidos | 5 | 23 | 1 |

O Google Trends esta operacional, mas parcial. O `pytrends` recebeu bloqueios `429 Too Many Requests`, entao a decisao atual e nao depender dele para a conclusao principal. No score, Trends pesa apenas 5% e eventos sem coleta ficam marcados explicitamente.

### Fontes dos eventos

| Pais | Verificados com URL | Referencia contextual | Total |
| --- | ---: | ---: | ---: |
| Argentina | 2 | 23 | 25 |
| Brasil | 3 | 31 | 34 |
| Estados Unidos | 10 | 19 | 29 |
| Projeto | 15 | 73 | 88 |

O top 15 do ranking global tem fonte verificavel com URL. Os demais eventos foram marcados como `contextual_reference`, sem URL individual, para registrar origem contextual sem fingir verificacao evento a evento.

## 3. Estrutura do projeto

```text
app.py
scripts/
  run_pipeline.py
  collect_*.py
  build_*.py
data/
  raw/
  processed/
docs/
  project_status_report.md
reports/
  project_audit.md
  figures/
```

### Camadas principais

| Camada | Arquivos principais | Funcao |
| --- | --- | --- |
| Coleta | `collect_bcb_sgs.py`, `collect_fred.py`, `collect_bluelytics.py`, `collect_world_bank.py`, `collect_trends*.py` | baixa dados externos |
| Preparacao | `prepare_political_events.py`, `build_economic_indicators_unified.py` | padroniza eventos e indicadores |
| Normalizacao | `build_normalized_economic_indicators.py`, `build_normalized_event_impact.py` | cria base comparavel por z-score |
| Analise | `build_event_statistical_tests.py`, `build_historical_robustness.py`, `build_event_shock_persistence.py` | mede significancia, raridade e persistencia |
| Event study | `build_event_study_series.py`, `build_event_study_aggregates.py` | cria curvas individuais e agregadas |
| Score | `build_event_final_score.py` | consolida componentes em ranking explicavel |
| Auditoria | `build_project_audit.py`, `build_event_sources_template.py`, `build_trends_coverage.py` | registra lacunas e cobertura |
| App | `app.py` | Streamlit com leitura simples, tecnica e aprendizado |

## 4. Logica metodologica

### Fluxo analitico

1. Coletar indicadores por pais e fonte.
2. Unificar schema com pais, data, frequencia, indicador, valor, unidade e fonte.
3. Normalizar cada serie dentro de seu proprio pais e indicador.
4. Cruzar eventos com janelas antes/depois de 30, 90, 180 e 365 dias.
5. Calcular movimento absoluto, percentual e padronizado.
6. Medir significancia aproximada com p-value ajustado por FDR.
7. Medir robustez historica por percentil contra movimentos semelhantes.
8. Medir contaminacao por eventos proximos.
9. Medir persistencia do choque.
10. Construir curvas de event study individuais e agregadas por categoria.
11. Consolidar score final.

### Score atual

Versao: `score_v1_1_trends_partial`.

| Componente | Peso | Interpretacao |
| --- | ---: | --- |
| Impacto | 35% | tamanho do maior movimento padronizado |
| Robustez historica | 25% | raridade do movimento frente ao historico |
| Significancia | 15% | evidencia estatistica aproximada com FDR |
| Persistencia | 15% | se o choque persiste ou volta rapido ao normal |
| Google Trends | 5% | atencao publica, quando coletada |
| Contaminacao | -5% | penalidade por eventos proximos na janela |

O ranking agora usa posicoes sequenciais e inclui:

- `score_tier`: faixa qualitativa do score;
- `score_caveat`: alerta metodologico, como cluster de eventos, ausencia de Trends ou data imprecisa.

Top 15 global atual:

| Rank | Pais | Evento | Score | Faixa | Alerta |
| ---: | --- | --- | ---: | --- | --- |
| 1 | BRA | Teto do ICMS dos combustiveis | 88,0 | muito alto | contaminacao moderada |
| 2 | USA | CARES Act | 83,2 | muito alto | cluster de eventos proximos |
| 3 | USA | American Rescue Plan | 81,3 | muito alto | contaminacao moderada |
| 4 | USA | Pandemia Covid | 80,3 | muito alto | cluster; sem Trends; data mensal |
| 5 | USA | Corte emergencial de juros do Fed | 80,3 | muito alto | cluster; sem Trends |
| 6 | USA | Fed leva juros a zero e relanca QE | 80,3 | muito alto | cluster; sem Trends |
| 7 | USA | Inflation Reduction Act | 75,1 | alto | contaminacao moderada; sem Trends |
| 8 | USA | Invasao do Capitolio | 74,8 | alto | cluster de eventos proximos |
| 9 | USA | Infrastructure Investment and Jobs Act | 74,5 | alto | sem Trends |
| 10 | ARG | Primarias com Milei forte | 72,0 | alto | contaminacao moderada; data mensal |
| 11 | BRA | Aprovacao da PEC dos Precatorios | 70,7 | alto | contaminacao moderada; sem Trends |
| 12 | ARG | Eleicao Milei | 70,7 | alto | cluster de eventos proximos |
| 13 | USA | Primeiro corte de juros do Fed desde 2008 | 69,8 | alto | sem Trends |
| 14 | BRA | Inicio do ciclo de alta da Selic | 69,4 | alto | contaminacao moderada; sem Trends |
| 15 | USA | Fed faz alta de 75 pontos-base | 69,1 | alto | contaminacao moderada; sem Trends |

## 5. App e UX

O app Streamlit esta funcional em `app.py`.

Principais views:

- visao por pais;
- comparacao entre paises;
- metodologia.

Na visao por pais, a leitura esta organizada em abas:

- `Evento`;
- `Padroes`;
- `Score`;
- `Rankings`;
- `Anual`.

Os toggles de conteudo estao funcionais:

- `Simples`: leitura direta, com menos detalhe tecnico;
- `Tecnico`: mostra formulas, fontes, codigo e limites;
- `Meu aprendizado`: explica conceitos como z-score, ranking e comparacao internacional.

Estado mobile: melhorado, mas nao perfeito. Controles, abas, tabelas e graficos receberam ajustes responsivos. Ainda pode haver scroll horizontal em graficos/tabelas densas, o que e aceitavel para dashboard analitico, mas deve ser revisado visualmente antes de publicar.

## 6. Qualidade e robustez

### Pontos fortes

- Pipeline reprodutivel com `scripts/run_pipeline.py`.
- Separacao limpa entre dados brutos e processados.
- Eventos suficientes para leitura exploratoria por pais.
- Normalizacao correta para comparacao internacional.
- Curto prazo e anual tratados separadamente.
- Score explicavel e auditavel.
- Penalidade por contaminacao.
- Fontes verificadas no top 15.
- Google Trends tratado como camada parcial, nao como dependencia central.
- App com camadas simples, tecnica e pedagogica.

### Pontos fracos

- Nao e estudo causal formal.
- `app.py` esta grande e concentra muita responsabilidade.
- Google Trends esta incompleto por limite do Google/pytrends.
- Argentina tem poucos indicadores frequentes.
- Fontes individuais fora do top 15 ainda sao contextuais.
- Nao ha suite de testes automatizados.
- Alguns eventos com data mensal/anual exigem leitura menos pontual.

### Riscos interpretativos

- Ranking mede choque observado, nao importancia historica absoluta.
- Eventos em cluster, como COVID/Fed/estimulos, podem compartilhar o mesmo movimento economico.
- Eventos sem Trends nao sao menos importantes; apenas nao tiveram coleta de atencao publica.
- Indicadores anuais do World Bank servem para contexto macro, nao evento fino.

## 7. Como rodar

Pipeline padrao, sem refazer coletas externas:

```powershell
python scripts/run_pipeline.py
```

Pipeline sem gerar graficos HTML exploratorios:

```powershell
python scripts/run_pipeline.py --skip-charts
```

Pipeline com coletas externas:

```powershell
python scripts/run_pipeline.py --with-collection
```

App:

```powershell
python -m streamlit run app.py
```

Coleta incremental de Trends, quando for tentar novamente:

```powershell
python scripts/collect_trends_missing_batch.py --country-code BRA --batch-size 1 --sleep-seconds 120
python scripts/run_pipeline.py --skip-charts
```

## 8. Proximos passos

### Alta prioridade

1. Fazer teste visual final em desktop e mobile.
2. Revisar a narrativa do top ranking no app: deixar claro que o ranking mede choque observado, nao importancia historica.
3. Se for publicar, transformar este relatorio em texto publico mais curto.

### Media prioridade

1. Expandir fontes verificadas para alem do top 15, se o uso exigir auditoria evento a evento.
2. Criar metodologia especifica para eventos `year` e `year_range`.
3. Extrair partes do `app.py` para modulos auxiliares.
4. Adicionar filtros de N minimo nas curvas agregadas por categoria.

### Baixa prioridade

1. Retomar Google Trends em outro momento, com lotes de 1 evento e pausa longa.
2. Expandir Argentina com inflacao mensal, juros, risco pais ou combustiveis.
3. Criar testes automatizados basicos para scripts centrais.
4. Inicializar git e fazer commit limpo, se esta pasta for a versao definitiva.

## 9. Veredito

O projeto esta pronto como demonstracao tecnica robusta e honesta. Para portfolio, falta principalmente acabamento visual final e narrativa publica. Para artigo academico, faltariam fontes individuais completas, controles causais mais fortes, placebo windows e metodologia formal para eventos longos.

O melhor proximo movimento nao e adicionar nova funcionalidade. E validar UX, ajustar texto de interpretacao e preparar a versao final de apresentacao.
