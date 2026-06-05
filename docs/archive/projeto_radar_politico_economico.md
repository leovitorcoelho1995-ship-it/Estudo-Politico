# Projeto: Radar de Influência Política, Repercussão Orgânica e Impacto Econômico

## 1. Ideia central

O projeto vai analisar como decisões políticas, eventos históricos e crises públicas geram repercussão na sociedade, usando dados de interesse de busca, indicadores econômicos e contexto histórico.

A ideia principal não é provar que um lado político é melhor ou pior, nem medir intenção de voto diretamente. O objetivo é medir **atenção pública**, **repercussão orgânica** e **possíveis associações temporais** entre eventos políticos e mudanças econômicas.

Formulação principal:

> Como decisões políticas e eventos históricos relevantes geram picos de interesse público, quais termos surgem organicamente após esses eventos e como esses momentos se relacionam com indicadores econômicos?

---

## 2. Escopo recomendado

### Países

- Brasil
- Estados Unidos
- Argentina

### Período

- 2016 a 2026

### Justificativa do período

O recorte de 2016 a 2026 é forte porque cobre uma década recente de alta polarização política, grandes eleições, crises econômicas, pandemia, mudanças de governo, disputas institucionais e eventos com grande repercussão pública.

Esse período inclui:

- impeachment no Brasil;
- eleição de Trump;
- governo Bolsonaro;
- pandemia;
- alta global de inflação;
- eleição Lula x Bolsonaro;
- eleição de Milei;
- reformas econômicas;
- crises institucionais;
- debates sobre combustíveis, inflação, desemprego, juros e câmbio.

---

## 3. Conceito analítico correto

Evitar dizer:

> “Vou medir a influência da esquerda e da direita.”

Melhor dizer:

> “Vou medir como o interesse público por temas, líderes e decisões políticas evoluiu ao longo do tempo e quais eventos parecem ter gerado maior repercussão.”

O Google Trends não mede apoio político, intenção de voto ou adoção ideológica. Ele mede interesse relativo de busca.

Portanto, o projeto deve analisar:

- picos de atenção;
- duração da repercussão;
- termos que surgiram organicamente;
- associação temporal com eventos;
- possível relação com indicadores econômicos;
- diferença entre países;
- personalização política em líderes;
- repercussão econômica, institucional, social ou ideológica.

---

## 4. Pergunta principal do projeto

> Quais decisões políticas e eventos históricos geraram maior repercussão orgânica na sociedade e quais indicadores econômicos mudaram ao redor desses eventos?

---

## 5. Hipóteses possíveis

### Hipótese 1

Eventos políticos com impacto direto no bolso da população geram maior repercussão orgânica em buscas econômicas.

Exemplos:

- gasolina;
- inflação;
- dólar;
- desemprego;
- auxílio;
- impostos;
- juros.

### Hipótese 2

A política recente é mais personalizada em líderes do que em partidos ou ideologias.

Exemplo:

- buscas por “Lula” e “Bolsonaro” podem superar buscas por “PT”, “PL”, “esquerda” e “direita”.
- buscas por “Trump” podem superar buscas por “Republican” ou “conservative”.
- buscas por “Milei” podem superar buscas por “liberalismo” ou “derecha”.

### Hipótese 3

Crises institucionais geram picos curtos e explosivos, enquanto decisões econômicas geram repercussão mais longa.

Exemplos:

- 8 de janeiro no Brasil: pico institucional forte e curto.
- alta da gasolina: repercussão econômica mais sustentada.
- inflação na Argentina: interesse persistente.

### Hipótese 4

Eventos eleitorais geram picos previsíveis, mas eventos inesperados podem gerar picos mais intensos.

Exemplos:

- facada em Bolsonaro;
- invasão do Capitólio;
- crise cambial argentina;
- protestos;
- escândalos.

---

## 6. Metodologia geral

O fluxo ideal do projeto é:

```text
Eventos políticos relevantes
        ↓
Termos sementes
        ↓
Google Trends Related Queries / Rising
        ↓
Descoberta de termos orgânicos
        ↓
Séries temporais desses termos
        ↓
Indicadores econômicos
        ↓
Análise de repercussão
        ↓
Dashboard em Streamlit
```

A lógica é começar pelos acontecimentos relevantes e depois descobrir organicamente quais termos cresceram ao redor deles.

---

## 7. Diferença entre abordagem tradicional e abordagem proposta

### Abordagem tradicional

```text
Escolher termos fixos → Buscar no Google Trends → Comparar gráficos
```

Problema:

- limita a análise;
- depende muito da escolha inicial;
- pode ignorar termos que surgiram espontaneamente;
- pode forçar narrativa.

### Abordagem proposta

```text
Detectar eventos relevantes → Usar termos sementes → Descobrir buscas relacionadas em ascensão → Analisar repercussão
```

Vantagens:

- mais investigativo;
- menos enviesado;
- revela termos inesperados;
- melhor storytelling;
- mais forte para portfólio.

---

## 8. Fontes de dados

### Google Trends

Uso principal:

- interesse ao longo do tempo;
- termos relacionados;
- consultas em ascensão;
- comparação por país;
- possível análise regional.

Limitação:

- índice relativo, não volume absoluto;
- o valor 100 representa o pico dentro do recorte escolhido;
- não mede apoio político;
- não mede intenção de voto;
- termos com baixo volume podem gerar dados instáveis.

### GDELT

Uso possível:

- detectar eventos políticos relevantes;
- identificar notícias de maior repercussão;
- filtrar eventos por país, data, tema e cobertura;
- analisar tom e volume de cobertura midiática.

Fonte específica:

- GDELT GKG tone, para capturar tom agregado da cobertura jornalística e comparar variações de humor midiático ao redor dos eventos.

### Fontes adicionais consideradas

- Bluelytics, para câmbio oficial e dólar blue na Argentina;
- World Bank API, para indicadores macroeconômicos comparáveis entre países;
- Gallup, para medidas internacionais de opinião pública, confiança e percepção social;
- Latinobarómetro, para opinião pública e percepção política na América Latina;
- GDELT GKG tone, para tom da cobertura midiática internacional;
- IMF, para séries macroeconômicas, dívida, inflação e comparações internacionais.

### Indicadores econômicos

#### Brasil

- Banco Central do Brasil
- IBGE
- ANP
- IPEAData
- Tesouro Nacional
- B3/Ibovespa

Indicadores:

- IPCA;
- Selic;
- dólar;
- gasolina;
- diesel;
- desemprego;
- PIB;
- salário mínimo real;
- dívida pública;
- Ibovespa.

Códigos SGS do Banco Central:

- 433: IPCA;
- 11: Selic;
- 1: taxa de câmbio;
- 24369: gasolina.

#### Estados Unidos

- FRED
- EIA
- Bureau of Labor Statistics
- Bureau of Economic Analysis
- Federal Reserve

Indicadores:

- CPI;
- gasoline price;
- Fed Funds Rate;
- unemployment;
- GDP;
- S&P 500;
- federal deficit;
- consumer confidence;
- real wages.

#### Argentina

- INDEC;
- Banco Central de la República Argentina;
- World Bank;
- bases econômicas internacionais.

Indicadores:

- inflação mensal e anual;
- dólar oficial;
- dólar blue, se houver fonte confiável;
- PIB;
- desemprego;
- pobreza;
- salário real;
- combustíveis;
- reservas internacionais;
- risco país.

---

## 9. Eventos políticos iniciais

## Brasil

```text
2016-08-31 | Impeachment Dilma | política institucional
2016-12-15 | Teto de gastos | fiscal
2017-07-13 | Reforma trabalhista | mercado de trabalho
2018-04-07 | Prisão de Lula | eleição/justiça
2018-09-06 | Facada em Bolsonaro | eleição/crise
2018-10-28 | Eleição Bolsonaro | eleição
2019-11-12 | Reforma da Previdência | fiscal
2020-03-11 | Pandemia Covid | crise externa
2020-04-02 | Auxílio emergencial | fiscal/social
2021-04-27 | CPI da Covid | crise política
2021-2022 | Alta dos combustíveis | energia/inflação
2022-06-23 | Teto do ICMS dos combustíveis | energia/fiscal
2022-10-30 | Eleição Lula | eleição
2023-01-08 | Atos de 8 de janeiro | crise institucional
2023-05-16 | Mudança na política de preços da Petrobras | energia
2023-08-31 | Novo arcabouço fiscal | fiscal
2024-10 | Eleições municipais | eleição
2025-2026 | Cenário fiscal, juros, inflação e crescimento | macroeconomia
```

## Estados Unidos

```text
2016-11-08 | Eleição Trump | eleição
2017-12-22 | Tax Cuts and Jobs Act | fiscal
2018-03 | Tarifas comerciais contra China | comércio
2020-03 | Pandemia Covid | crise externa
2020-03-27 | CARES Act | fiscal/social
2020-11-03 | Eleição Biden | eleição
2021-01-06 | Invasão do Capitólio | crise institucional
2021-03-11 | American Rescue Plan | fiscal/social
2021-2022 | Alta inflacionária | inflação
2022-03 | Ciclo de alta de juros do Fed | monetário
2022-08-16 | Inflation Reduction Act | fiscal/energia
2024-11 | Eleição presidencial | eleição
2025-2026 | Decisões econômicas recentes | macroeconomia
```

## Argentina

```text
2016-2019 | Governo Mauricio Macri | política econômica
2018-06 | Acordo com FMI | dívida/câmbio
2019-10-27 | Eleição Alberto Fernández | eleição
2020-03 | Pandemia Covid | crise externa
2020-2022 | Controles cambiais e crise inflacionária | câmbio/inflação
2022-03 | Renegociação com FMI | dívida
2023-08 | Primárias com Milei forte | eleição
2023-11-19 | Eleição Milei | eleição
2023-12 | Desvalorização inicial do peso | câmbio/inflação
2024 | Ajuste fiscal e reformas | fiscal/social
2024 | Protestos e greve geral | reação social
2025-2026 | Continuidade das reformas | macroeconomia
```

---

## 10. Termos sementes

Termos sementes são termos iniciais usados para puxar termos relacionados e consultas em ascensão no Google Trends.

## Brasil

### Política geral

```text
Lula
Bolsonaro
Dilma
Temer
PT
PL
esquerda
direita
comunismo
fascismo
democracia
golpe
STF
Congresso
impeachment
```

### Economia

```text
gasolina
diesel
Petrobras
inflação
dólar
Selic
juros
desemprego
auxílio emergencial
Auxílio Brasil
Bolsa Família
reforma trabalhista
reforma da previdência
ICMS gasolina
```

## Estados Unidos

```text
Trump
Biden
Obama
Kamala Harris
Republican
Democrat
left wing
right wing
liberal
conservative
socialism
capitalism
MAGA
woke
inflation
gas prices
tax cuts
China tariffs
immigration
Fed rates
```

## Argentina

```text
Milei
Macri
Cristina Kirchner
Alberto Fernández
Peronismo
Kirchnerismo
izquierda
derecha
liberalismo
inflación
dólar blue
FMI
ajuste
nafta
pobreza
devaluación
```

---

## 11. Descoberta orgânica de termos

Para cada evento político, o projeto deve buscar:

- related queries;
- rising queries;
- related topics;
- breakout terms;
- termos associados ao evento;
- termos econômicos que cresceram depois.

Exemplo:

### Evento: mudança na política de preços da Petrobras

Termos sementes:

```text
Petrobras
gasolina
diesel
combustíveis
```

Possíveis termos orgânicos descobertos:

```text
preço da gasolina hoje
ICMS gasolina
Petrobras dividendos
paridade internacional
reajuste gasolina
diesel hoje
```

### Evento: eleição de Milei

Termos sementes:

```text
Milei
dólar blue
inflación
devaluación
ajuste
```

Possíveis termos orgânicos:

```text
plan motosierra
dólar blue hoy
inflación argentina
devaluación peso
protestas Milei
```

---

## 12. Classificação da repercussão

Cada termo descoberto pode ser classificado em uma das categorias abaixo.

### Repercussão econômica

```text
gasolina
inflação
dólar
juros
desemprego
imposto
salário
auxílio
```

### Repercussão política

```text
Lula
Bolsonaro
Trump
Biden
Milei
Congresso
STF
impeachment
eleição
```

### Repercussão ideológica

```text
esquerda
direita
comunismo
fascismo
liberalismo
socialismo
conservadorismo
```

### Repercussão institucional

```text
STF
Suprema Corte
Capitólio
democracia
golpe
constituição
fraude eleitoral
```

### Repercussão social

```text
protesto
greve
pobreza
fome
auxílio
aposentadoria
```

---

## 13. Janelas de análise

Para cada evento, usar janelas de comparação.

### Curto prazo

```text
30 dias antes
data do evento
30 dias depois
```

### Médio prazo

```text
90 dias antes
data do evento
90 dias depois
```

### Longo prazo

```text
12 meses antes
data do evento
12 meses depois
```

Para decisões econômicas relevantes, como reforma, corte de impostos, teto de gastos ou mudança de política energética, o ideal é usar 12 meses antes e 12 meses depois.

Para crises e eventos inesperados, usar 30 ou 90 dias.

---

## 14. Métricas do projeto

## 14.1 Índice de atenção política

Mede o nível de interesse público por política em determinado período.

```text
Google Trends de líderes + partidos + ideologias + eventos políticos
```

Exemplo Brasil:

```text
Lula + Bolsonaro + PT + PL + esquerda + direita + STF + golpe
```

## 14.2 Índice de personalização política

Mede se a política está mais concentrada em líderes do que em partidos ou ideologias.

```text
buscas por líderes / buscas por partidos e ideologias
```

Exemplo Brasil:

```text
(Lula + Bolsonaro) / (PT + PL + esquerda + direita)
```

## 14.3 Índice de repercussão econômica

Mede o peso dos termos econômicos após eventos políticos.

```text
buscas por termos econômicos relacionados / buscas políticas totais
```

Exemplo:

```text
(gasolina + inflação + dólar + juros) / (Lula + Bolsonaro + governo + eleição)
```

## 14.4 Índice de choque econômico

Mede a intensidade de variação econômica ao redor de um evento.

```text
abs(variação inflação)
+ abs(variação câmbio)
+ abs(variação gasolina)
+ abs(variação desemprego)
```

## 14.5 Índice de evento dominante

Mede o tamanho do pico gerado por um evento.

```text
pico do termo na semana do evento / média das 12 semanas anteriores
```

## 14.6 Duração da repercussão

Mede quanto tempo o interesse ficou acima da média histórica.

```text
número de dias ou semanas acima de X% da média anterior
```

## 14.7 Meia-vida do interesse

Mede quanto tempo o interesse levou para cair 50% após o pico.

```text
data em que o interesse caiu para metade do pico - data do pico
```

---

## 15. Estrutura de dados

## 15.1 Tabela `political_events`

| Campo | Descrição |
|---|---|
| event_id | identificador único do evento |
| country | país |
| date | data do evento |
| event_name | nome do evento |
| category | categoria política/econômica |
| leader | líder ou governo relacionado |
| description | resumo do evento |
| source | fonte histórica/notícia |

Exemplo:

| event_id | country | date | event_name | category | leader |
|---|---|---|---|---|---|
| BR_2022_ICMS | Brasil | 2022-06-23 | Teto do ICMS dos combustíveis | energia/fiscal | Bolsonaro |
| BR_2023_PETROBRAS | Brasil | 2023-05-16 | Mudança na política de preços da Petrobras | energia | Lula |

## 15.2 Tabela `seed_terms`

| Campo | Descrição |
|---|---|
| event_id | evento relacionado |
| seed_term | termo inicial |
| language | idioma |
| country | país |
| category | política, economia, social, institucional etc. |

## 15.3 Tabela `organic_terms`

| Campo | Descrição |
|---|---|
| event_id | evento relacionado |
| seed_term | termo semente |
| related_query | termo descoberto |
| growth | crescimento informado pelo Trends |
| type | rising, related, breakout |
| category | econômica, política, ideológica, institucional, social |

## 15.4 Tabela `trends_timeseries`

| Campo | Descrição |
|---|---|
| date | data |
| country | país |
| term | termo |
| interest | índice do Google Trends |
| category | categoria |
| event_id | evento próximo, se houver |

## 15.5 Tabela `economic_indicators`

| Campo | Descrição |
|---|---|
| date | data |
| country | país |
| indicator | indicador |
| value | valor |
| unit | unidade |
| source | fonte |

## 15.6 Tabela `event_impact_analysis`

| Campo | Descrição |
|---|---|
| event_id | evento |
| country | país |
| indicator | indicador econômico |
| value_before | valor antes |
| value_after | valor depois |
| variation_pct | variação percentual |
| window | janela usada |
| peak_term | termo com maior pico |
| peak_value | valor do pico |
| peak_date | data do pico |

---

## 16. Wireframe do Streamlit

## Página 1 — Visão Geral

Título:

> Radar de Influência Política, Repercussão Orgânica e Impacto Econômico

Cards principais:

- período analisado;
- países analisados;
- total de eventos políticos;
- total de termos orgânicos descobertos;
- maior pico de busca;
- evento com maior repercussão;
- indicador econômico mais volátil;
- país com maior volatilidade política.

Gráficos:

- linha temporal de interesse político;
- linha temporal de indicadores econômicos;
- heatmap país x ano x intensidade política;
- ranking de eventos por repercussão.

---

## Página 2 — Event Explorer

Filtros:

- país;
- ano;
- categoria;
- líder/governo;
- evento;
- janela de análise.

Exibe:

- descrição do evento;
- contexto histórico;
- termos sementes;
- indicadores econômicos relacionados;
- links/fonte;
- gráfico do período.

---

## Página 3 — Repercussão Orgânica

Objetivo:

Mostrar quais termos surgiram ou cresceram após cada evento.

Tabela:

| Termo descoberto | Crescimento | Tipo | Semente | Categoria |
|---|---:|---|---|---|
| preço gasolina hoje | +350% | rising | gasolina | econômica |
| ICMS gasolina | breakout | rising | gasolina | econômica |
| Petrobras dividendos | +180% | rising | Petrobras | econômica |

Gráficos:

- ranking de termos orgânicos;
- nuvem de termos;
- barras por categoria;
- comparação entre sementes e termos descobertos.

---

## Página 4 — Antes e Depois

Objetivo:

Comparar o período anterior e posterior ao evento.

Visual principal:

```text
Linha 1: interesse de busca
Linha 2: indicador econômico
Linha vertical: data do evento
```

Filtros:

- evento;
- termo;
- indicador econômico;
- janela: 30, 90, 180 ou 365 dias.

Métricas:

- média antes;
- média depois;
- variação percentual;
- data do pico;
- duração do pico;
- possível evento relacionado.

---

## Página 5 — Gasolina e Política

Página dedicada ao impacto de combustíveis.

Indicadores:

- gasolina;
- diesel;
- petróleo internacional;
- câmbio;
- inflação;
- buscas por termos relacionados.

Comparações:

- Brasil: gasolina x Petrobras x Lula/Bolsonaro;
- EUA: gas prices x Biden/Trump;
- Argentina: nafta x Milei/FMI/inflación.

Perguntas:

- quando combustível gerou maior repercussão?
- qual país teve maior sensibilidade?
- o pico de buscas acompanhou o aumento real do preço?
- a repercussão foi curta ou sustentada?

---

## Página 6 — Inflação, Câmbio e Governo

Objetivo:

Comparar indicadores macroeconômicos com interesse político.

Gráficos:

- inflação x busca por presidente;
- dólar/câmbio x busca por governo;
- juros x busca por economia;
- desemprego x busca por auxílio/benefícios.

---

## Página 7 — Comparativo Internacional

Objetivo:

Comparar Brasil, EUA e Argentina.

Gráficos:

- eventos por ano;
- inflação por país;
- interesse político por país;
- índice de personalização política;
- índice de repercussão econômica;
- ranking dos maiores picos;
- ranking dos eventos de maior choque econômico.

---

## Página 8 — Detector de Picos

Funcionalidade:

O usuário escolhe:

- país;
- termo;
- indicador econômico;
- janela temporal.

O app retorna:

- maior pico;
- data do pico;
- média anterior;
- crescimento vs baseline;
- duração da repercussão;
- evento político mais próximo;
- indicador econômico relacionado;
- explicação automática.

Exemplo de output:

```text
Termo: gasolina
País: Brasil
Pico: outubro de 2021
Evento próximo: crise de preços dos combustíveis
Crescimento vs média anterior: calcular
Indicador relacionado: preço médio da gasolina
```

---

## Página 9 — Metodologia e Limitações

Conteúdo:

- Google Trends mede interesse relativo, não volume absoluto;
- correlação temporal não prova causalidade;
- termos políticos mudam de significado por país;
- indicadores econômicos têm causas múltiplas;
- eventos foram classificados manualmente ou semi-automaticamente;
- o projeto mede repercussão, não apoio político;
- o projeto não mede intenção de voto diretamente;
- janelas antes/depois podem distorcer eventos longos.

---

## 17. Roadmap de execução

## Fase 1 — MVP Brasil

Objetivo:

Criar o pipeline com apenas Brasil.

Período:

- 2016 a 2026.

Eventos iniciais:

```text
Impeachment Dilma
Reforma trabalhista
Facada em Bolsonaro
Reforma da Previdência
Auxílio emergencial
CPI da Covid
Teto do ICMS dos combustíveis
Mudança na política de preços da Petrobras
Atos de 8 de janeiro
Eleição Lula x Bolsonaro
```

Indicadores:

```text
gasolina
IPCA
dólar
Selic
desemprego
Ibovespa
```

Entregáveis:

- dataset de eventos;
- coleta de Trends;
- termos orgânicos;
- gráficos básicos;
- primeiro Streamlit funcional.

---

## Fase 2 — Expandir para EUA

Adicionar:

- eleição Trump;
- Tax Cuts;
- guerra comercial;
- pandemia;
- CARES Act;
- eleição Biden;
- Capitólio;
- American Rescue Plan;
- inflação;
- juros do Fed;
- Inflation Reduction Act.

Indicadores:

```text
gas prices
CPI
Fed Funds Rate
unemployment
GDP
S&P 500
```

---

## Fase 3 — Expandir para Argentina

Adicionar:

- governo Macri;
- acordo FMI;
- eleição Alberto Fernández;
- pandemia;
- controles cambiais;
- eleição Milei;
- desvalorização;
- ajuste fiscal;
- reformas;
- protestos.

Indicadores:

```text
inflação
dólar oficial
dólar blue
PIB
desemprego
pobreza
salário real
combustíveis
```

---

## Fase 4 — Criar métricas próprias

Implementar:

- índice de atenção política;
- índice de personalização política;
- índice de repercussão econômica;
- índice de choque econômico;
- índice de evento dominante;
- duração da repercussão;
- meia-vida do interesse.

---

## Fase 5 — Finalizar storytelling

Entregáveis finais:

- Streamlit publicado;
- repositório GitHub;
- notebook de coleta/tratamento;
- README profissional;
- artigo curto no LinkedIn;
- vídeo curto explicando o projeto;
- prints do dashboard para portfólio.

---

## 18. Nome do projeto

Opções:

1. Political Attention & Economic Impact Monitor
2. Radar Político-Econômico
3. Da Busca ao Bolso
4. Política em Dados
5. Google Trends e Economia Política
6. Radar de Repercussão Política
7. Political Event Impact Tracker
8. Politics, Search & Economy

Nome recomendado para portfólio:

> Political Attention & Economic Impact Monitor

Subtítulo:

> A data project analyzing political events, organic search behavior and economic indicators across Brazil, USA and Argentina.

Versão em português:

> Radar de Influência Política e Impacto Econômico

Subtítulo:

> Um projeto de dados que analisa eventos políticos, repercussão orgânica no Google Trends e indicadores econômicos no Brasil, EUA e Argentina.

Decisão atual sobre portfólio:

> Não colocar no portfólio por enquanto.

Justificativa:

O tema envolve política recente, comparação entre países e interpretação pública de eventos sensíveis. Mesmo com metodologia cuidadosa, o projeto pode ser lido como posicionamento político ou gerar ruído desnecessário em processos seletivos. A decisão é manter como estudo técnico interno, prova de conceito ou material de aprendizado, e só transformar em portfólio se a narrativa ficar claramente metodológica, neutra e orientada a dados.

---

## 19. Stack recomendada

### Principal

- Python
- Pandas
- Streamlit
- Plotly
- Google Trends / pytrends
- CSV ou Parquet
- GitHub

Estrutura de pastas:

```text
data/
  raw/        # dados brutos baixados das APIs e fontes originais
  processed/  # dados limpos, padronizados e prontos para análise/dashboard
```

### Complementar

- APIs econômicas;
- GDELT;
- notebooks Jupyter;
- Power BI apenas como versão executiva opcional.

Decisão recomendada:

> Usar Streamlit como ferramenta principal.

Motivo:

O projeto é investigativo, interativo e analítico. Streamlit permite criar uma experiência mais rica do que um dashboard estático, com detector de picos, filtros, explicações, tabelas e storytelling.

---

## 20. Versão final ideal

A versão final deve parecer uma ferramenta de investigação.

O usuário entra no app, escolhe um país e um evento, e vê:

1. o que aconteceu;
2. quais termos surgiram organicamente;
3. quais buscas explodiram;
4. quanto tempo a repercussão durou;
5. quais indicadores econômicos se moveram;
6. se a repercussão foi econômica, política, ideológica, institucional ou social;
7. como esse evento se compara a outros países.

Resumo do conceito final:

> Eventos políticos primeiro. Termos orgânicos depois. Indicadores econômicos por último.

Essa estrutura evita forçar narrativa e deixa os dados mostrarem o que realmente repercutiu.
