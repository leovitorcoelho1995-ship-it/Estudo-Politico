# Memoria de Contexto do Projeto: Radar Politico-Economico

Este documento e a memoria operacional do projeto. Ele registra o que ja esta implementado, o que entrou no plano e o que ainda falta fazer.

## 1. Visao Geral

- Objetivo: analisar associacoes temporais entre eventos politicos/historicos, atencao publica no Google Trends e indicadores economicos no Brasil, Estados Unidos e Argentina.
- Recorte temporal: 2016 a 2026.
- Principio metodologico: comparar paises por trajetorias, z-score e choques relativos, evitando comparar valores brutos entre economias estruturalmente diferentes.
- Status geral: prototipo analitico funcional em Streamlit, com pipeline de dados, normalizacao, impacto por evento, camada inicial de Trends e auditoria automatica.

## 2. Estado Atual

### Coleta de dados

- Brasil: `collect_bcb_sgs.py` coleta IPCA, Selic, cambio e gasolina via BCB SGS.
- Estados Unidos: `collect_fred.py` coleta CPI, Fed Funds Rate, desemprego, gasolina e PIB real via FRED.
- Argentina: `collect_bluelytics.py` coleta dolar oficial e dolar blue diarios via Bluelytics.
- Internacional: `collect_world_bank.py` coleta indicadores anuais comparaveis via World Bank API, usando `mrv=10` para buscar os anos mais recentes disponiveis.
- Atencao publica: `collect_trends.py` coleta Google Trends por evento e salva series em `data/raw/trends/`.

### Processamento

- Base economica unificada: `data/processed/economic_indicators_unified.csv`.
- Base economica normalizada: `data/processed/economic_indicators_normalized.csv`.
- Eventos processados: `data/processed/political_events_processed.csv`.
- Fontes dos eventos: `data/raw/political_event_sources.csv` e auditoria `data/processed/event_sources_audit.csv`.
- Impacto de curto prazo: `data/processed/event_economic_impact.csv` e `data/processed/event_economic_impact_normalized.csv`.
- Significancia estatistica: `data/processed/event_economic_impact_significance.csv`.
- Contaminacao por eventos proximos: `data/processed/event_window_contamination.csv`.
- Persistencia do choque: `data/processed/event_shock_persistence.csv`.
- Event study centrado no dia 0: `data/processed/event_study_series.csv`.
- Curvas agregadas de event study por categoria: `data/processed/event_study_category_aggregates.csv`.
- Score final dos eventos: `data/processed/event_final_score.csv`.
- Impacto anual: `data/processed/annual_event_impact.csv`.
- Robustez historica: `data/processed/event_economic_impact_robustness.csv`.
- Rankings: `ranking_short_term_impacts*`, `ranking_annual_impacts*` e `ranking_annual_context_by_country_year.csv`.
- Trends normalizado: `data/processed/trends_normalized.csv`.
- Alinhamento evento-Trends: `data/processed/trends_event_alignment.csv`.
- Cobertura de Trends: `data/processed/trends_coverage.csv`.
- Auditoria: `reports/project_audit.md` e tabelas `audit_*`.

### App Streamlit

O `app.py` ja possui:

- Navegacao principal em barra horizontal de controles segmentados para view, pais e nivel de detalhe.
- Modos `leitura simples`, `modo tecnico` e `meu aprendizado`.
- Tabela clicavel de eventos com `st.dataframe(..., on_select="rerun", selection_mode="single-row")`.
- Coluna `impacto` na tabela de eventos.
- Grafico de indicadores normalizados com marcacao do evento selecionado.
- Secao Evento x Movimento em duas colunas, com linha do indicador e mini-cards laterais de direcao/magnitude.
- Secao `03b` de Google Trends, com serie normalizada, pico de interesse, timing do pico e intensidade em z-score.
- Comparacao entre paises com dados anuais do World Bank.
- Secao de metodologia e `learning_expander` em pontos importantes.
- Notas de cobertura deixando claro que series frequentes chegam a 2026 e World Bank anual esta limitado a `WORLD_BANK_MAX_YEAR = 2024`.
- Correcoes de seguranca/robustez no HTML dinamico com `html.escape`.

## 3. O Que Ja Foi Implementado dos Docs

- Bloco 1: navegacao e estrutura geral. Implementado, com ajuste posterior de sidebar para barra horizontal.
- Bloco 2: interatividade evento -> grafico. Implementado parcialmente/majoritariamente: tabela clicavel, callout e coluna de impacto existem. Scroll automatico por ancora/JS ainda nao foi priorizado.
- Bloco 3: visualizacao Evento x Movimento. Implementado.
- Bloco 4: cobertura e periodo dos dados. Implementado.
- Bloco 5: modo Meu Aprendizado. Implementado em secoes centrais.
- Bloco 6: Google Trends. Implementado como camada inicial; coleta expandida para parte dos eventos, com dados normalizados e secao no app.
- Bloco 7: Argentina com indicadores frequentes. Implementado via Bluelytics.
- Bloco 8: correcoes de codigo. Implementado: chave duplicada removida, `html.escape` aplicado e `section_header` usa `replace(..., 1)`.

## 4. Gaps Atuais

### Alta prioridade

- Cobertura de eventos: target metodologico passa a ser 20-30 eventos por pais, com entrada quando o evento (1) gerou cobertura de primeira pagina por 3+ dias consecutivos ou (2) foi decisao formal de politica economica/institucional com efeito mensuravel esperado em pelo menos um indicador da base.
- Inferencia estatistica: adicionar teste t de Welch ou Mann-Whitney para comparar janelas antes/depois, com `p_value`, intervalo de confianca e correcao FDR/Benjamini-Hochberg para multiplos testes.
- Controle de confundidores: tornar mais explicito que eventos no mesmo periodo compartilham ambiente macroeconomico; propor mitigacoes como residualizar tendencia, dummies de ano ou flags de janelas contaminadas.
- Persistencia do choque: modelar se o choque decaiu, persistiu ou reverteu com meia-vida do choque e/ou grafico de event study centrado no dia 0.
- Integracao da robustez nos rankings: a tabela `event_economic_impact_robustness.csv` ja aparece no app, mas ainda precisa entrar nos rankings agregados.
- Eventos longos: criar metodologia separada para eventos `year` e `year_range`, que nao devem ser tratados como um ponto unico.
- Google Trends avancado: usar melhor `related_queries`, termos organicos, duracao da repercussao, meia-vida, delay ate o pico e metricas de atencao.

### Media prioridade

- Correlacao Trends x indicador com lag: calcular se o pico de atencao antecede, coincide ou sucede o pico economico.
- Analise de defasagem: identificar janelas de resposta de 30, 60, 90 e 180 dias.
- Sobreposicao de eventos: marcar janelas contaminadas por eventos proximos.
- Volatilidade condicional: comparar desvio-padrao rolling antes/depois para saber se o evento aumentou incerteza mesmo sem mudar a media.
- Contagion index: testar correlacao cruzada entre paises durante janelas de crise.
- Storytelling editorial: fortalecer o fluxo contexto -> evento -> movimento -> interpretacao -> limite metodologico.

### Baixa prioridade / acabamento

- Heatmap evento x indicador x janela.
- Indice composto de turbulencia por evento.
- Robustez por sub-periodo.
- Criar script unico de pipeline para rodar coleta, processamento, graficos e auditoria.
- Mover dicionarios de labels para `src/` ou arquivo de configuracao.
- Normalizar encoding dos markdowns antigos que ainda contem caracteres quebrados.
- Preparar prints e texto neutro para LinkedIn/portfolio.
- Inicializar git, se esta pasta for a pasta definitiva do projeto.

## 5. Proxima Etapa Recomendada

Adicionar inferencia estatistica ao motor de impacto antes/depois:

1. Criar colunas de significancia em `event_economic_impact.csv` ou em uma tabela derivada: `test_name`, `p_value`, `effect_size`, intervalo de confianca e observacoes antes/depois.
2. Aplicar correcao FDR/Benjamini-Hochberg por familia de testes, por exemplo pais + indicador + janela.
3. Expor no app a diferenca entre intensidade do movimento, raridade historica e significancia estatistica.

Essa etapa aumenta a credibilidade metodologica porque separa choque grande, choque raro e diferenca estatisticamente defensavel.

## 6. Revisao Tecnica Recebida

### Pontos ja tratados ou parcialmente tratados

- Encoding quebrado no `app.py`: corrigido na interface e validado no navegador (`hasBroken: false`). Foi adicionado `# -*- coding: utf-8 -*-` no topo do arquivo como protecao explicita.
- Argentina no curto prazo: o app ja tem aviso generico quando nao ha calculo de curto prazo e a metodologia registra cobertura parcial; ainda falta deixar esse aviso mais especifico para Argentina e eventos `year`/`year_range`.
- Robustez historica: ja existe tabela de percentil e raridade historica, mas ainda falta integrar de modo mais forte aos rankings.

### Pontos tecnicos pendentes

- `nearby_event_hover_labels` ainda usa loop por data e por evento; em bases maiores pode virar gargalo. Refatorar com estrategia vetorizada ou precomputada.
- A largura dos mini-cards usa `abs_value / 3.0` como escala fixa. Documentar o limite de 3 desvios-padrao ou trocar para escala dinamica baseada no maximo observado do evento/pais.
- `WORLD_BANK_MAX_YEAR = 2024` ainda esta hardcoded. Melhor derivar do dado real (`max(year)` para World Bank) ou mover para configuracao.

### Pilares para nivel academico real

- Pilar 1: inferencia estatistica com testes antes/depois, p-value, intervalo de confianca e correcao de multiplos testes.
- Pilar 2: controle de confundidores com tendencia, dummies temporais, janelas contaminadas e limitacoes explicitas.
- Pilar 3: persistencia do choque com meia-vida, retorno a faixa normal e event study.

## 7. Registro de Progresso

### 2026-06-04

- Pipeline economico multi-pais montado.
- App Streamlit funcional criado.
- Normalizacao, impactos, rankings e auditoria implementados.
- Bloco 1 concluido e depois ajustado de sidebar para barra horizontal.
- Bloco 2 majoritariamente concluido.
- Bloco 3 concluido.
- Bloco 4 concluido.
- Bloco 5 implementado nas secoes principais.
- Bloco 6 iniciado e expandido: scripts de Trends criados, coleta real para parte dos eventos, 2.707 linhas normalizadas e 36 alinhamentos de pico registrados no ultimo processamento.
- Bloco 7 concluido com Bluelytics.
- Bloco 8 concluido.
- Memoria do projeto atualizada para refletir o estado real do codigo.
- Teste de robustez historica criado em `scripts/build_historical_robustness.py`; saida com 521 linhas, 43 movimentos raros, 83 acima do comum, 319 comuns e 76 insuficientes.
- App atualizado para carregar `event_economic_impact_robustness.csv`, mostrar robustez na tabela de eventos e exibir percentil historico/raridade nos detalhes do evento selecionado.
- Inferencia estatistica inicial criada em `scripts/build_event_statistical_tests.py`; gera p-value aproximado, correcao FDR e rotulo de significancia. Saida atual: 521 linhas, com 316 fortes, 22 moderadas, 20 fracas, 72 nao significativas e 91 insuficientes.
- App atualizado para carregar `event_economic_impact_significance.csv` e mostrar p-value FDR/significancia nos detalhes do evento selecionado.
- Controle inicial de confundidores criado em `scripts/build_event_window_contamination.py`; gera contagem de eventos do mesmo pais em janelas de 30, 90 e 180 dias.
- Rankings de curto prazo enriquecidos com nivel de contaminacao da janela, e app atualizado para mostrar a coluna `contaminacao` e aviso quando o evento selecionado tem eventos proximos.
- Persistencia do choque criada em `scripts/build_event_shock_persistence.py`; mede pico pos-evento, dias ate pico, retorno para faixa normal e rotulo de persistencia.
- App atualizado para mostrar persistencia na tabela detalhada do evento selecionado.
- Event study criado em `scripts/build_event_study_series.py`; gera serie normalizada de -180 a +365 dias ao redor do evento.
- App atualizado com grafico de estudo de evento no detalhe do evento selecionado.
- Curvas agregadas por categoria criadas em `scripts/build_event_study_aggregates.py`; agregam media, mediana, p25, p75, eventos e observacoes por pais, categoria e dia relativo.
- App atualizado com comparacao de curva media por categoria em cada pais.
- Score final criado em `scripts/build_event_final_score.py`; combina impacto, robustez, significancia, persistencia, Google Trends e penalidade por contaminacao.
- App atualizado com ranking sintetico e decomposicao do score por pais.
- Score final versionado; pesos salvos em `data/processed/event_final_score_config.csv`.
- View `Comparar paises` atualizada com comparacao multi-pais de curto prazo por categoria, usando curvas medias de event study por pais.
- Google Trends recebeu auditoria de cobertura em `scripts/build_trends_coverage.py`; termos-semente foram expandidos para eventos novos e a primeira coleta incremental elevou Argentina de 3 para 10 eventos com Trends. Google retornou 429 em parte do lote, entao a coleta restante deve ser feita em lotes menores e com pausa maior.
- Primeira melhoria de UX/mobile aplicada: CSS responsivo reforcado para hero, KPIs, controles, tabelas e graficos; visao por pais recebeu mapa compacto da leitura para orientar a sequencia evento -> padroes -> score -> rankings -> anual.
- Visao por pais refatorada em abas reais: `Evento`, `Padroes`, `Score`, `Rankings` e `Anual`. As abas foram validadas no navegador sem traceback, mantendo a selecao do evento no topo.
- View `Metodologia` atualizada para refletir o estado real do projeto: criterios de inclusao de eventos, limites de causalidade, eventos longos, contaminacao, pesos do score final, cobertura por pais, cobertura Google Trends e fluxo tecnico completo.
- Orquestrador criado em `scripts/run_pipeline.py`; por padrao roda processamento completo sem refazer coletas externas. Use `--with-collection` para incluir BCB/FRED/Bluelytics/World Bank e `--skip-charts` para pular graficos HTML.
- Estrutura de fontes por evento criada em `scripts/build_event_sources_template.py`; gera `data/raw/political_event_sources.csv` com 88 eventos e status inicial `pending`, alem de auditoria em `event_sources_audit.csv`.
- Auditoria do projeto atualizada: gap global agora aponta `Google Trends parcial e fontes dos eventos pendentes`, em vez de robustez estatistica.
- Coleta incremental de Trends operacionalizada em `scripts/collect_trends_missing_batch.py`, com filtros por pais, tamanho de lote, pausa e dry-run.
- Auditoria consolidada do estado atual criada em `docs/current_state_audit.md`, cobrindo estado, logica, estrutura, robustez, UX, documentacao e pendencias reais.
- Plano de coleta de fontes criado em `docs/source_collection_plan.md`, priorizando top score, Brasil, EUA e Argentina, com criterio minimo para publicacao defensavel.
- Score ajustado para `score_v1_1_trends_partial`: peso de Trends caiu de 15% para 5% enquanto a cobertura esta parcial; impacto e robustez receberam mais peso. O CSV agora explicita `has_trends_data` e `trends_score_note`.
- Cobertura de eventos revisada: Argentina recebeu 13 eventos pontuais adicionais entre 2018 e 2024, chegando a 25 eventos totais e 20 com cobertura de curto prazo. A expansao priorizou FMI/divida, controles cambiais, saltos do peso/dolar blue, trocas de ministro da Economia e marcos das reformas de Milei.
- Cobertura de eventos revisada: Brasil recebeu 16 eventos pontuais adicionais entre 2016 e 2024, chegando a 34 eventos totais e 32 com cobertura de curto prazo. A expansao priorizou Copom/Selic, choques fiscais, combustiveis, Petrobras, transicao de governo, reformas e crises politico-institucionais com canal economico claro.
- Cobertura de eventos revisada: Estados Unidos recebeu 16 eventos pontuais adicionais entre 2016 e 2024, chegando a 29 eventos totais e 27 com cobertura de curto prazo. A expansao priorizou Fed/juros, estimulos fiscais, tarifas EUA-China, teto da divida, choque bancario de 2023 e marcos de politica economica.
- Nota de cobertura Argentina: os 5 eventos sem curto prazo sao todos `year` ou `year_range` (`Governo Mauricio Macri`, `Controles cambiais e crise inflacionaria`, `Ajuste fiscal e reformas`, `Protestos e greve geral`, `Continuidade das reformas`). Portanto a lacuna e metodologica por granularidade temporal do evento, nao por ausencia da Bluelytics, que cobre dolar oficial e dolar blue em frequencia diaria.
- Fontes dos eventos atualizadas: top 15 do `score_rank_global` recebeu `source_status = verified` com URL verificavel em `data/raw/political_event_sources.csv`; os outros 73 eventos foram marcados como `contextual_reference`, sem URL individual, para registrar origem contextual sem inventar verificacao.
- Pipeline validado apos fontes: `python scripts/run_pipeline.py --skip-charts` concluiu sem erro, com 88 eventos, 79 eventos de curto prazo, 1.182 linhas de impacto e auditoria de fontes atualizada.
- Google Trends Brasil: tentativa de lote com 5 eventos e pausa de 45s coletou `BRA_2016_08_31` com sucesso, mas Google retornou 429 nos quatro seguintes. Depois, em modo `batch-size 1`, coletou `BRA_2016_10_19`; o evento seguinte (`BRA_2016_12_15`) voltou a receber 429. Apos pipeline, Trends normalizado ficou em 4.153 linhas, alinhamentos em 63 e cobertura Brasil em 8 eventos coletados, 23 pendentes de coleta e 3 sem seed.
- Calibracao do ranking/score: pesos foram mantidos em `score_v1_1_trends_partial`, mas o ranking deixou de usar `dense rank` com empates visuais e passou a gerar posicoes sequenciais com desempate por score/data/pais/evento. Foram adicionadas as colunas `score_tier` e `score_caveat` para separar intensidade do score de alertas metodologicos como contaminacao, ausencia de Trends e precisao mensal/anual da data. O app passou a exibir faixa e alerta na aba `Score`; a metodologia foi alinhada aos pesos reais: impacto 35%, robustez 25%, significancia 15%, persistencia 15%, Trends 5% e contaminacao -5%.
