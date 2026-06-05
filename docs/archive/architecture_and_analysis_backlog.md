# Revisao de arquitetura e backlog analitico

> Nota de manutencao: este documento e historico. O estado operacional mais atual esta em `docs/project_memory.md`, `docs/post_report_update.md` e `reports/project_audit.md`. Alguns itens abaixo ja foram implementados: Google Trends inicial, robustez historica, persistencia do choque, event study, score final, expansao de eventos e `run_pipeline.py`.


Este documento resume o estado atual do projeto, os pontos fortes da arquitetura, as lacunas metodologicas e as proximas analises que mais aumentam valor.

## Arquitetura atual

### 1. Coleta

Fontes conectadas:

- BCB SGS, para Brasil;
- FRED, para Estados Unidos;
- World Bank API, para Brasil, Estados Unidos e Argentina.

Status:

- Brasil tem boa cobertura de curto prazo para cambio, juros, inflacao e gasolina;
- Estados Unidos tem boa cobertura para gasolina, juros, CPI, desemprego e PIB real;
- Argentina tem World Bank anual e cambio diario pela Bluelytics, com dolar oficial e dolar blue.

### 2. Processamento

O projeto ja possui uma camada economica unificada:

```text
data/processed/economic_indicators_unified.csv
```

E uma camada normalizada:

```text
data/processed/economic_indicators_normalized.csv
```

A normalizacao e o ponto metodologico mais importante do projeto, porque evita comparar valores brutos entre paises estruturalmente diferentes.

### 3. Eventos

Eventos politicos estao organizados em:

```text
data/processed/political_events_processed.csv
```

Cada evento tem:

- pais;
- data inicial;
- data final;
- precisao da data;
- categoria;
- subcategoria.

### 4. Impacto economico

Ha duas leituras:

- curto prazo, usando dados diarios, semanais, mensais ou trimestrais;
- anual, usando World Bank para comparacao entre os tres paises.

Arquivos principais:

```text
data/processed/event_economic_impact_normalized.csv
data/processed/annual_event_impact.csv
```

### 5. App

O `app.py` ja tem:

- visao por pais;
- comparacao entre paises;
- modo leitura simples;
- modo tecnico;
- tabela de eventos;
- destaque visual de evento no grafico;
- grafico antes/depois do evento selecionado.

## Lacunas atuais

### Lacuna 1: atencao publica ainda nao entrou

O conceito original inclui Google Trends, termos sementes e termos organicos. A arquitetura economica esta avancada, mas a camada de atencao publica ainda nao foi implementada.

Impacto:

- o projeto ainda mede eventos e economia, mas nao mede repercussao organica;
- falta responder "o que as pessoas passaram a buscar depois do evento?".

Prioridade: alta.

### Lacuna 2: Argentina com curto prazo parcial

Argentina ja esta coberta por World Bank anual e Bluelytics diaria para:

- cambio oficial;
- dolar blue.

Ainda faltam series frequentes de:

- inflacao mensal;
- taxa de juros;
- combustiveis;
- risco pais.

Impacto:

- Argentina entra na leitura macro anual;
- Argentina entra no motor de 30, 90, 180 e 365 dias para eventos com data exata ou mes aproximado;
- eventos marcados apenas como ano ou periodo continuam pedindo uma metodologia separada.

Prioridade: alta.

### Lacuna 3: eventos longos precisam de outra metodologia

Eventos como "Alta dos combustiveis 2021-2022" ou "Governo Mauricio Macri 2016-2019" nao devem ser tratados como um ponto unico.

Impacto:

- ficam fora da analise curta;
- a leitura anual fica ampla demais.

Prioridade: media.

### Lacuna 4: ainda nao ha teste de robustez

Hoje o motor calcula antes/depois, mas ainda nao compara o movimento do evento com janelas aleatorias ou periodos sem evento.

Impacto:

- nao sabemos se um movimento foi realmente incomum em relacao a outros periodos;
- rankings podem capturar volatilidade normal.

Prioridade: alta.

### Lacuna 5: storytelling ainda pode ficar mais editorial

O app esta visualmente melhor, mas ainda pode evoluir para uma narrativa:

```text
contexto -> evento -> movimento -> interpretacao -> limite metodologico
```

Prioridade: media.

## Analises recomendadas

### 1. Indice de atencao publica

Fonte:

- Google Trends.

Objetivo:

- medir interesse relativo por evento, lider, tema economico e termos relacionados.

Metricas:

- pico de interesse;
- media antes/depois;
- duracao da repercussao;
- meia-vida do interesse;
- termos relacionados em ascensao.

Valor para o projeto:

- conecta politica, sociedade e economia;
- aproxima o projeto do conceito original.

### 2. Repercussao organica de termos

Fonte:

- Google Trends related queries / rising.

Objetivo:

- descobrir quais termos surgem ao redor de eventos, sem depender apenas de termos escolhidos manualmente.

Exemplo:

```text
evento: mudanca na politica de precos da Petrobras
termos possiveis: gasolina, Petrobras dividendos, preco dos combustiveis, defasagem internacional
```

Valor:

- melhora storytelling;
- reduz vies de escolher apenas termos obvios.

### 3. Persistencia do choque economico

Objetivo:

- medir se o indicador voltou ao padrao historico depois do evento.

Metricas:

- dias ate voltar para faixa normal;
- permanencia acima de 1 desvio-padrao;
- maior distancia do padrao apos o evento.

Valor:

- diferencia pico curto de mudanca prolongada.

### 4. Teste de significancia por janelas historicas

Objetivo:

- comparar a mudanca antes/depois do evento com mudancas de janelas semelhantes em outros momentos da serie.

Metricas:

- percentil historico do choque;
- flag de movimento raro;
- ranking robusto.

Valor:

- evita chamar de "impacto" algo que acontece frequentemente.

### 5. Analise de defasagem

Objetivo:

- testar se alguns indicadores respondem depois de 30, 60, 90 ou 180 dias.

Metricas:

- janela de maior choque;
- atraso maximo observado;
- diferenca entre paises.

Valor:

- melhora a narrativa: alguns eventos afetam busca imediatamente, economia depois.

### 6. Sobreposicao de eventos

Objetivo:

- identificar quando varios eventos estao proximos e podem contaminar a leitura.

Metricas:

- eventos nos 30/90 dias antes;
- eventos nos 30/90 dias depois;
- flag de janela contaminada.

Valor:

- aumenta honestidade metodologica.

### 7. Tipologia de eventos

Objetivo:

- comparar eventos por categoria: eleicao, fiscal, energia, crise institucional, pandemia.

Metricas:

- choque medio por categoria;
- indicador mais sensivel por categoria;
- pais mais sensivel por categoria.

Valor:

- transforma casos isolados em padroes.

### 8. Camada de midia e tom

Fonte:

- GDELT GKG tone.

Objetivo:

- medir volume e tom de cobertura midiatico ao redor dos eventos.

Valor:

- separa interesse publico, cobertura midiaticia e indicadores economicos.

### 9. Camada argentina de curto prazo

Fontes candidatas:

- BCRA;
- INDEC;
- Ambito / series publicas de dolar blue, se houver fonte confiavel;
- IMF para series macro complementares.

Objetivo:

- incluir Argentina no motor curto de eventos.

Valor:

- fortalece comparacao internacional.

### 10. Score final de evento

Objetivo:

- criar uma metrica sintetica para ordenar eventos.

Componentes possiveis:

- choque economico padronizado;
- duracao do choque;
- pico de atencao publica;
- volume de termos organicos;
- cobertura midiaticia;
- penalidade por janela contaminada.

Valor:

- vira storytelling principal do dashboard.

## Melhorias de arquitetura

### 1. Script unico de pipeline

Hoje os scripts precisam ser rodados em sequencia manual. Um script `run_pipeline.py` poderia orquestrar tudo.

Beneficio:

- reduz erro operacional;
- facilita reproducibilidade.

### 2. Auditoria automatica do projeto

Criar um script que gere:

- cobertura por pais;
- cobertura por fonte;
- eventos cobertos por curto prazo;
- eventos sem cobertura;
- lacunas por frequencia.

Beneficio:

- deixa as limitacoes visiveis;
- ajuda a priorizar proximas etapas.

### 3. Camada `src/`

Hoje muita logica fica em scripts independentes. Funcoes comuns poderiam ir para `src/`.

Beneficio:

- evita duplicacao;
- melhora manutencao.

### 4. Dicionarios de labels fora do app

Os labels amigaveis hoje estao em `app.py`. Podem virar CSV ou modulo de configuracao.

Beneficio:

- facilita manutencao;
- evita misturar UX com logica.

## Prioridade recomendada

1. Auditoria automatica de cobertura.
2. Google Trends para atencao publica.
3. Persistencia do choque economico.
4. Teste de significancia por janelas historicas.
5. Sobreposicao/contaminacao de eventos.
6. Dados frequentes da Argentina.
7. GDELT tone.
8. Score final de evento.
