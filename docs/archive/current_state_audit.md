# Auditoria completa do estado atual

Data da auditoria: 2026-06-04

## 1. Resumo executivo

O projeto esta em bom estado para um prototipo analitico robusto. Ele ja saiu da fase de prova de conceito simples e virou uma aplicacao exploratoria com pipeline reprodutivel, score sintetico, auditoria de lacunas, comparacao multi-pais, event study individual/agregado, Google Trends parcial e UX organizada em abas.

O nucleo metodologico esta coerente: o estudo nao compara valores brutos entre economias diferentes; ele compara desvios em relacao ao padrao historico de cada pais/indicador. Isso e a decisao tecnica mais importante do projeto.

O maior risco ainda e interpretativo, nao tecnico: os resultados mostram associacao temporal robusta, nao causalidade. O app ja comunica isso melhor do que antes, mas essa ressalva deve continuar presente em qualquer uso publico.

## 2. Estado quantitativo

### Cobertura de eventos

| Pais | Eventos totais | Eventos curto prazo | Eventos anuais | Indicadores frequentes | Indicadores anuais | Lacuna principal |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Argentina | 25 | 20 | 25 | 2 | 4 | eventos longos ou sem janela curta |
| Brasil | 34 | 32 | 34 | 4 | 5 | eventos longos ou sem janela curta |
| Estados Unidos | 29 | 27 | 29 | 5 | 5 | eventos longos ou sem janela curta |
| Projeto | 88 | 79 | 88 | 21 | 14 | Google Trends parcial; fontes verificadas no top 15 e contextuais no restante |

Leitura: o volume de eventos agora e suficiente para exploracao por pais e para subgrupos, principalmente em `economy`. Categorias menores como `external_shock` e `society` ainda devem ser lidas como estudos de caso, nao como padroes estatisticamente fortes.

### Pipeline e artefatos principais

O pipeline atual produz:

- `economic_indicators_unified.csv`
- `economic_indicators_normalized.csv`
- `political_events_processed.csv`
- `event_economic_impact_normalized.csv`
- `event_economic_impact_significance.csv`
- `event_economic_impact_robustness.csv`
- `event_window_contamination.csv`
- `event_shock_persistence.csv`
- `event_study_series.csv`
- `event_study_category_aggregates.csv`
- `trends_normalized.csv`
- `trends_event_alignment.csv`
- `trends_coverage.csv`
- `event_final_score.csv`
- `event_final_score_config.csv`
- rankings e auditorias.

O orquestrador `scripts/run_pipeline.py` foi criado e validado com `--skip-charts`.

## 3. Logica metodologica

### Decisoes corretas

1. Normalizacao por pais/indicador.
   - Evita comparar inflacao, juros, cambio e desemprego em niveis brutos entre economias muito diferentes.

2. Separacao entre curto prazo e anual.
   - Series frequentes entram em janelas antes/depois.
   - World Bank entra para comparacao anual, com defasagem assumida.

3. Eventos longos fora do motor curto.
   - `year` e `year_range` nao sao tratados como pontos exatos.

4. Score final explicavel.
   - O score nao e caixa-preta: cada componente e exportado e mostrado.

5. Penalidade por contaminacao.
   - Eventos proximos nao invalidam a leitura, mas reduzem confianca causal.

6. Google Trends opcional.
   - Eventos sem Trends nao quebram o pipeline.

### Limites metodologicos

1. Nao ha desenho causal formal.
   - O estudo mede associacao temporal.
   - Nao controla completamente tendencia, sazonalidade, regime macro ou shocks simultaneos.

2. Curadoria de eventos ainda e manual.
   - O criterio existe e o top 15 do ranking ja tem fonte individual verificada; os demais eventos estao marcados como referencia contextual generica.

3. Argentina e estreita no curto prazo.
   - A leitura frequente se apoia em dolar oficial e dolar blue.
   - Falta inflacao mensal, juros, risco pais ou combustiveis.

4. Estados Unidos tem frequencias misturadas.
   - Mensal, semanal e trimestral reduzem a precisao diaria em alguns event studies.

5. Trends esta parcial.
   - O score de atencao publica ainda favorece eventos com coleta disponivel.

## 4. Estrutura de codigo

### Pontos fortes

- Scripts pequenos e especializados.
- Pipeline reprodutivel por `run_pipeline.py`.
- Separacao clara entre `data/raw`, `data/processed`, `scripts`, `docs`, `reports`.
- App centralizado, mas funcional.
- Auditorias salvas em CSV/Markdown.

### Pontos fracos

- `app.py` esta grande e concentra labels, UX, graficos e regras de apresentacao.
- Ainda nao ha camada `src/` para funcoes comuns.
- Alguns documentos historicos ainda existem com contexto antigo, embora agora tenham nota de manutencao.
- Nao ha testes automatizados formais; a verificacao tem sido por compile, pipeline e app local.

### Risco tecnico

Baixo a moderado. O projeto roda e compila, mas o tamanho do `app.py` vai dificultar manutencoes futuras. A proxima melhora arquitetural natural e extrair:

- labels;
- formatadores;
- graficos;
- tabelas;
- blocos de metodologia;
- helpers de score.

## 5. Robustez analitica

O projeto ja mede:

- intensidade padronizada;
- significancia estatistica aproximada;
- p-value FDR;
- robustez historica por percentil;
- contaminacao por eventos proximos;
- persistencia do choque;
- event study individual;
- curva media por categoria;
- score final `score_v1_1_trends_partial`.

Isso e forte para exploracao. O que falta para subir o nivel e:

- controles por tendencia;
- dummies de ano/regime;
- sazonalidade;
- janelas contaminadas como covariavel;
- comparacao com janelas placebo;
- documentacao de fontes por evento.

## 6. Score final

Versao atual: `score_v1_1_trends_partial`.

Pesos:

| Componente | Peso |
| --- | ---: |
| impacto | 0,35 |
| robustez | 0,25 |
| significancia | 0,15 |
| persistencia | 0,15 |
| Trends | 0,05 |
| contaminacao | -0,05 |

O peso de Trends foi reduzido enquanto a cobertura esta parcial. Eventos sem Trends aparecem explicitamente com `has_trends_data = False` e `trends_score_note = missing_collection_zeroed_low_weight`.

Top global atual:

| Rank | Pais | Evento | Score |
| ---: | --- | --- | ---: |
| 1 | BRA | Teto do ICMS dos combustiveis | 88,0 |
| 2 | USA | CARES Act | 83,2 |
| 3 | USA | American Rescue Plan | 81,3 |
| 4 | USA | Corte emergencial de juros do Fed | 80,3 |
| 5 | USA | Fed leva juros a zero e relanca QE | 80,3 |

Leitura: o score esta operacional e explicavel. A calibracao final ainda deve ser qualitativa. O topo ainda traz `Teto do ICMS dos combustiveis` como #1, o que pode estar tecnicamente correto mas e menos forte como ancora narrativa internacional.

## 7. Google Trends

Cobertura atual:

| Pais | Coletados | Pendentes coleta | Sem seed |
| --- | ---: | ---: | ---: |
| ARG | 10 | 10 | 5 |
| BRA | 6 | 25 | 3 |
| USA | 5 | 23 | 1 |

Foi criado `scripts/collect_trends_missing_batch.py`, que permite coletar lotes pequenos com pausa. Isso e importante porque o Google retornou 429 em parte da coleta.

Estado: operacional, mas incompleto.

Risco: enquanto Trends estiver parcial, o componente `trends_score` poderia favorecer eventos ja coletados. A mitigacao atual e reduzir o peso para 5% e explicitar no CSV quais eventos nao tem Trends.

## 8. Fontes dos eventos

Foi criada a estrutura:

- `data/raw/political_event_sources.csv`
- `data/processed/event_sources_audit.csv`
- `data/processed/event_sources_audit_summary.csv`

Estado atual:

| Pais | Verificados com URL | Referencia contextual | Total |
| --- | ---: | ---: | ---: |
| ARG | 2 | 23 | 25 |
| BRA | 3 | 31 | 34 |
| USA | 10 | 19 | 29 |

Decisao correta: nenhum link foi inventado automaticamente. O top 15 do score global tem fonte individual verificavel; os demais foram marcados como `contextual_reference`, sem URL, para nao simular precisao que ainda nao foi auditada.

Risco residual: fora do top 15, a credibilidade externa da curadoria de eventos ainda depende da confianca no dataset e da metodologia, nao de verificacao individual por URL.

## 9. App e UX

### Estado atual

O app tem:

- filtros principais no topo;
- modos `Simples`, `Tecnico`, `Meu aprendizado`;
- visao por pais;
- comparacao entre paises;
- metodologia;
- abas reais na visao por pais:
  - `Evento`;
  - `Padroes`;
  - `Score`;
  - `Rankings`;
  - `Anual`.

### Pontos fortes

- A selecao do evento no topo cria uma narrativa clara.
- As abas reduziram a sensacao de pagina infinita.
- A comparacao multi-pais de curto prazo agora usa as curvas agregadas.
- O modo tecnico e o modo aprendizado existem e funcionam como camadas de profundidade.
- O CSS mobile foi melhorado para controles, tabelas e graficos.

### Pontos fracos

- Graficos largos ainda dependem de scroll horizontal em mobile.
- Algumas tabelas sao densas para tela pequena.
- O modo aprendizado ainda nao cobre com a mesma profundidade todas as secoes novas.
- `app.py` concentra muita responsabilidade.

## 10. Documentacao

### Fortes

- `docs/project_memory.md` esta atualizado.
- `docs/post_report_update.md` registra o que mudou depois do relatorio.
- `docs/current_state_audit.md` consolida o estado atual.
- README tem comandos do pipeline.

### Fracos

- Existem docs historicos com conteudo antigo. Eles receberam nota de manutencao, mas ainda podem confundir se lidos fora de ordem.
- O projeto ainda precisa de uma documentacao mais limpa de "versao publica" se for para portfolio.

## 11. Pendencias reais

### Alta prioridade

1. Completar Google Trends em lotes pequenos.
2. Expandir fontes verificadas para alem do top 15, se a versao publica exigir auditoria evento a evento.
3. Revisar qualitativamente o ranking `score_v1_1_trends_partial`.

### Media prioridade

1. Criar metodologia especifica para eventos `year` e `year_range`.
2. Extrair partes do `app.py` para modulos auxiliares.
3. Adicionar filtros de N minimo nas curvas agregadas por categoria.
4. Adicionar testes automatizados simples para scripts centrais.

### Baixa prioridade

1. Melhorar mobile visualmente com screenshots reais em mais viewports.
2. Preparar narrativa de portfolio.
3. Expandir Argentina com mais indicadores frequentes.

## 12. Veredito

O projeto esta tecnicamente solido como aplicacao analitica exploratoria. A estrutura atual permite demonstrar raciocinio de dados, pipeline, metodologia, UX e capacidade de auditoria. Ainda nao e um estudo causal academico, mas ja e um dashboard analitico honesto, reprodutivel e bem instrumentado.

O proximo salto de qualidade nao e adicionar mais graficos. E completar Trends e, se necessario, ampliar fontes verificadas para alem do top 15, porque isso melhora a confiabilidade externa do estudo.
