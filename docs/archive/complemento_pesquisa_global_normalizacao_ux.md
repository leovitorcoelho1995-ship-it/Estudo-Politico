# Complemento do Projeto: Pesquisa Global, Normalização entre Países, Influência dos EUA e UX Robusta

Este documento complementa o projeto principal **Radar de Influência Política, Repercussão Orgânica e Impacto Econômico**.

A ideia aqui não é pivotar o projeto. A estrutura original continua correta:

```text
Eventos políticos relevantes
        ↓
Termos sementes
        ↓
Descoberta de termos orgânicos no Google Trends
        ↓
Séries temporais de interesse público
        ↓
Indicadores econômicos
        ↓
Análise de repercussão
        ↓
Streamlit investigativo
```

Este complemento adiciona quatro camadas:

1. Pesquisa global/multipaís no Streamlit.
2. Normalização correta para comparação entre países.
3. Módulo de influência dos EUA na América Latina.
4. Melhorias de robustez metodológica e UX.

---

## 1. O projeto está indo na direção certa?

Sim.

O projeto **não deve ser pivotado**. O caminho atual está ficando mais forte porque saiu de uma ideia genérica:

> “Comparar esquerda e direita no Google Trends.”

E virou uma proposta mais robusta:

> “Analisar como eventos políticos, decisões econômicas e choques externos geram repercussão orgânica em buscas públicas e como esses movimentos se relacionam com indicadores econômicos.”

Essa evolução é positiva.

O projeto agora tem:

- pergunta de pesquisa mais clara;
- metodologia mais defensável;
- diferencial analítico;
- possibilidade de análise internacional;
- uso forte de Streamlit;
- comparação política e econômica;
- camada de descoberta orgânica de termos;
- potencial de investigação aplicada.

O ponto importante é manter o núcleo simples e adicionar módulos com cuidado, sem perder o foco.

---

## 2. Estrutura final recomendada

A estrutura completa do projeto deve ter três blocos analíticos principais.

### Bloco A — Repercussão doméstica

Pergunta:

> Como eventos e decisões internas repercutem dentro do próprio país?

Exemplos:

- Brasil: impeachment, Petrobras, ICMS combustíveis, eleição Lula x Bolsonaro, 8 de janeiro.
- EUA: eleição Trump/Biden, Capitólio, tax cuts, inflação, juros do Fed.
- Argentina: eleição Milei, desvalorização, FMI, inflação, reformas.

### Bloco B — Repercussão econômica

Pergunta:

> Quando a política mexe no bolso, como o interesse público muda?

Indicadores:

- gasolina;
- inflação;
- dólar/câmbio;
- juros;
- desemprego;
- PIB;
- salário real;
- pobreza;
- bolsa/mercado financeiro.

### Bloco C — Influência externa dos EUA

Pergunta:

> Eventos políticos e econômicos dos EUA geram respostas econômicas e de busca no Brasil e na Argentina?

Exemplos de choques dos EUA:

- alta de juros do Fed;
- eleição presidencial americana;
- guerra comercial EUA-China;
- inflação americana;
- preço do petróleo;
- crises financeiras;
- dólar forte;
- decisões de política externa.

---

## 3. Pesquisa global no Streamlit

O Streamlit pode funcionar como uma ferramenta de investigação multipaís.

Ele não limita a análise a um país. O que define o alcance global é:

- base de eventos;
- base de termos;
- base de indicadores econômicos;
- coleta do Google Trends;
- fontes de notícias;
- estrutura de comparação.

O app pode ter três modos.

### 3.1 Modo 1 — Exploração por país

Fluxo:

```text
Escolher país
↓
Escolher evento
↓
Ver termos orgânicos
↓
Ver indicadores econômicos
↓
Ver repercussão antes/depois
```

Exemplo de filtros:

```text
País: Brasil / EUA / Argentina
Evento: eleição, reforma, crise, decisão econômica
Indicador: gasolina, inflação, câmbio, desemprego
Janela: 30 / 90 / 180 / 365 dias
```

Esse deve ser o modo principal do app.

### 3.2 Modo 2 — Comparação entre países

Fluxo:

```text
Escolher tipo de evento equivalente
↓
Comparar Brasil, EUA e Argentina
↓
Usar métricas normalizadas
```

Eventos equivalentes:

| Tipo de evento | Brasil | EUA | Argentina |
|---|---|---|---|
| Eleição presidencial | 2022 | 2020 / 2024 | 2023 |
| Crise institucional | 8 de janeiro | Capitólio | protestos/reformas |
| Inflação/combustível | 2021–2022 | 2021–2022 | 2023–2024 |
| Política fiscal | teto/arcabouço | tax cuts/IRA | ajuste fiscal |
| Choque cambial | dólar/juros | Fed/dólar | dólar blue/desvalorização |

Importante:

> A comparação deve ser feita por comportamento relativo, não por volume bruto.

### 3.3 Modo 3 — Mapa global/contextual

O app pode ter um mapa com:

- Brasil;
- EUA;
- Argentina;
- conexões de influência;
- eventos globais;
- choques externos.

Objetivo do mapa:

- mostrar contexto;
- facilitar navegação;
- conectar eventos dos EUA a respostas na América Latina;
- enriquecer a UX.

Não é necessário analisar o mundo inteiro no MVP. O mapa pode começar com três países e uma camada de influência externa.

---

## 4. Problema da normalização entre países

O Google Trends não entrega volume absoluto de buscas. Ele entrega índices relativos.

Isso significa que:

```text
100 no Brasil ≠ 100 na Argentina ≠ 100 nos EUA
```

O valor 100 representa o pico relativo dentro daquele país, período e configuração de busca.

Portanto, a comparação errada seria:

```text
Brasil buscou mais por inflação do que Argentina.
```

A comparação correta seria:

```text
Na Argentina, o interesse por inflação ficou X vezes acima da média anterior.
No Brasil, ficou Y vezes acima da média anterior.
Nos EUA, ficou Z vezes acima da média anterior.
```

---

## 5. Como resolver a normalização

A solução é comparar cada país contra o seu próprio baseline.

Em vez de comparar valores absolutos do Google Trends, o projeto deve usar métricas derivadas.

### 5.1 Event Spike Ratio

Mede o tamanho do pico em relação ao nível normal anterior.

Fórmula:

```text
Event Spike Ratio = pico pós-evento / média pré-evento
```

Exemplo:

```text
Média das 12 semanas antes: 20
Pico pós-evento: 100
Event Spike Ratio = 100 / 20 = 5x
```

Interpretação:

> O interesse ficou 5 vezes acima do padrão recente daquele país.

Essa métrica é uma das principais para comparação internacional.

### 5.2 Abnormal Interest Index

Mede o quanto o interesse ficou acima do esperado.

Fórmula absoluta:

```text
Abnormal Interest = interesse observado - média pré-evento
```

Fórmula percentual:

```text
Abnormal Interest % = (interesse observado - média pré-evento) / média pré-evento
```

### 5.3 Duração da repercussão

Mede por quanto tempo o interesse permaneceu acima do normal.

Fórmula:

```text
Número de dias/semanas acima de 150% da média pré-evento
```

Interpretação:

- pico curto: evento explosivo, mas passageiro;
- pico longo: repercussão sustentada;
- interesse persistente: tema estrutural.

### 5.4 Meia-vida do interesse

Mede quanto tempo o interesse levou para cair 50% depois do pico.

Fórmula:

```text
Meia-vida = data em que interesse caiu para 50% do pico - data do pico
```

### 5.5 Volatilidade política

Mede se a série é instável, cheia de picos, ou estável.

Fórmula:

```text
Volatilidade = desvio padrão da série / média da série
```

### 5.6 Share of Political Attention

Mede a composição interna da repercussão.

Fórmula:

```text
Share por categoria = interesse da categoria / interesse total dos termos relacionados
```

Categorias:

- política;
- econômica;
- institucional;
- social;
- ideológica.

### 5.7 Delay até o pico

Mede quantos dias o interesse demorou para atingir o pico depois do evento.

Fórmula:

```text
Delay até pico = data do pico - data do evento
```

Interpretação:

- delay curto: reação imediata;
- delay médio: repercussão mediada por notícias/debates;
- delay longo: evento com efeito acumulado ou narrativa prolongada.

---

## 6. Tipos corretos de comparação internacional

### 6.1 Comparação interna

Pergunta:

> Dentro de cada país, quais eventos geraram maior repercussão?

É a comparação mais segura.

### 6.2 Comparação por evento equivalente

Pergunta:

> Como eventos parecidos se comportam em países diferentes?

Exemplos:

- eleição presidencial;
- crise institucional;
- inflação;
- alta de combustíveis;
- reforma fiscal;
- choque cambial.

### 6.3 Comparação por indicador econômico

Pergunta:

> Quando a inflação sobe, o interesse por inflação reage da mesma forma em cada país?

Exemplo de análise:

```text
Variação da inflação
vs
Variação do interesse por inflação
```

### 6.4 Comparação por categoria de repercussão

Pergunta:

> O evento gerou mais repercussão econômica, política, social ou institucional?

---

## 7. Módulo: influência dos EUA na América Latina

Este módulo deve ser adicionado como camada complementar, não como substituto da análise principal.

Nome sugerido:

> US Shock → Latin America Response

Pergunta:

> Eventos políticos e econômicos dos EUA provocam respostas econômicas e de busca no Brasil e na Argentina?

### 7.1 Eventos dos EUA relevantes

Eventos a considerar:

```text
Eleição presidencial americana
Alta de juros do Fed
Inflação americana
Dólar forte
Preço internacional do petróleo
Guerra comercial EUA-China
Crises bancárias/financeiras
Mudanças em política externa
Sanções/geopolítica
Pacotes fiscais americanos
```

### 7.2 Canais de influência

#### Canal 1 — Juros e dólar

Fluxo:

```text
Fed sobe juros
↓
dólar se fortalece
↓
moedas emergentes sofrem pressão
↓
real/peso podem se desvalorizar
↓
inflação e juros locais podem ser afetados
↓
buscas por dólar, inflação e juros aumentam
```

Indicadores:

- Fed Funds Rate;
- DXY;
- câmbio BRL/USD;
- câmbio ARS/USD;
- inflação local;
- juros locais.

Termos Brasil:

```text
dólar
Selic
inflação
juros
Banco Central
```

Termos Argentina:

```text
dólar blue
inflación
devaluación
Banco Central
FMI
```

#### Canal 2 — Petróleo e combustíveis

Fluxo:

```text
Choque no petróleo
↓
preço internacional do petróleo muda
↓
gasolina/diesel podem mudar
↓
inflação local pode ser afetada
↓
buscas por gasolina/combustível aumentam
```

Indicadores:

- preço do petróleo WTI/Brent;
- gasolina Brasil;
- gasolina EUA;
- combustíveis Argentina;
- inflação.

Termos Brasil:

```text
gasolina
Petrobras
diesel
preço gasolina
combustíveis
```

Termos EUA:

```text
gas prices
oil prices
inflation
Biden gas prices
```

Termos Argentina:

```text
nafta
combustibles
inflación
YPF
```

#### Canal 3 — Eleição americana e geopolítica

Fluxo:

```text
Eleição nos EUA
↓
mudança de expectativas globais
↓
mercado reage
↓
câmbio e bolsa podem se mover
↓
mídia local repercute
↓
buscas locais sobem
```

Indicadores:

- S&P 500;
- dólar;
- Ibovespa;
- risco país;
- câmbio;
- índices de mercado.

Termos locais:

```text
Trump
Biden
eleição EUA
dólar
bolsa
mercado financeiro
```

### 7.3 Métrica: Lag Response

Mede quantos dias Brasil/Argentina demoraram para reagir a um evento dos EUA.

Fórmula:

```text
Lag Response = data do pico local - data do evento dos EUA
```

### 7.4 Métrica: External Influence Score

Score para medir força da associação entre evento dos EUA e resposta local.

Critérios:

```text
+3 evento dos EUA ocorreu antes do pico local
+2 indicador global mudou no mesmo período
+2 termo local relacionado subiu
+1 Brasil e Argentina reagiram em janela parecida
+1 houve cobertura jornalística local citando EUA/Fed/petróleo
+1 impacto econômico local apareceu nos dados
```

Classificação:

```text
0–3 = influência fraca
4–6 = influência moderada
7–10 = influência forte
```

---

## 8. Robustez metodológica

Para o projeto parecer sério, cada associação evento-termo-indicador deve ter um nível de confiança.

### 8.1 Association Confidence Score

Score para medir se um pico de busca provavelmente está ligado a um evento.

Critérios:

```text
+3 pico ocorreu até 7 dias após o evento
+2 termo orgânico apareceu como rising/breakout
+2 termo tem relação semântica direta com o evento
+1 houve cobertura jornalística no período
+1 indicador econômico relacionado mudou
+1 pico se repetiu em termos relacionados
```

Classificação:

```text
0–3 = associação fraca
4–6 = associação média
7–10 = associação forte
```

Uso no app:

- mostrar selo visual;
- filtrar eventos por confiança;
- evitar conclusões fortes em associações fracas.

### 8.2 Separar evento, decisão e crise externa

Tipos recomendados:

| Tipo | Descrição | Exemplo |
|---|---|---|
| political_decision | decisão formal de governo | reforma, lei, mudança tributária |
| political_event | acontecimento político | eleição, CPI, protesto |
| economic_policy | política econômica | corte de impostos, juros, auxílio |
| institutional_crisis | crise institucional | Capitólio, 8 de janeiro |
| external_shock | choque externo | petróleo, Fed, pandemia |
| election | eleição | presidencial, parlamentar |
| social_reaction | reação social | greve, protesto, manifestação |

### 8.3 Evitar causalidade forte

Evitar:

```text
A decisão X causou aumento da gasolina.
```

Usar:

```text
Após a decisão X, houve variação Y no preço da gasolina, em um contexto marcado também por fatores como câmbio, petróleo e inflação global.
```

Ou:

```text
O evento X esteve temporalmente associado a um pico de interesse pelo termo Y.
```

### 8.4 Controle de fatores externos

Para indicadores econômicos, listar fatores relevantes.

Gasolina:

- petróleo internacional;
- câmbio;
- impostos;
- política de preços;
- logística;
- subsídios;
- choque externo.

Inflação:

- alimentos;
- energia;
- câmbio;
- juros;
- demanda;
- choque global;
- política fiscal.

Câmbio:

- juros internacionais;
- risco fiscal;
- commodities;
- fluxo de capital;
- política monetária;
- cenário externo.

Desemprego:

- ciclo econômico;
- sazonalidade;
- reforma trabalhista;
- pandemia;
- crescimento do PIB;
- informalidade.

---

## 9. UX robusta no Streamlit

O app deve parecer uma ferramenta de investigação, não apenas um painel.

### 9.1 Estrutura de navegação

Páginas recomendadas:

```text
1. Home / Executive Summary
2. Event Explorer
3. Organic Terms Discovery
4. Before & After
5. Economic Impact
6. Cross-Country Comparison
7. US Influence Layer
8. Methodology Lab
9. Data Explorer
```

### 9.2 Sidebar fixa

Filtros principais:

```text
Modo de análise
País
Ano
Tipo de evento
Evento
Categoria de repercussão
Indicador econômico
Janela temporal
Score mínimo de confiança
```

### 9.3 Página 1 — Home / Executive Summary

Objetivo:

Dar uma visão geral forte e imediata.

Componentes:

- mapa com Brasil, EUA e Argentina;
- ranking dos eventos com maior repercussão;
- ranking dos maiores choques econômicos;
- cards de resumo;
- botão para explorar evento.

Cards:

```text
Maior pico político
Maior repercussão econômica
Evento com maior duração
País mais volátil
Maior resposta a choque externo
Maior influência externa detectada
```

### 9.4 Página 2 — Event Explorer

Objetivo:

Permitir investigar um evento específico.

Layout:

```text
[Resumo do evento]
[Classificação do evento]
[Timeline com marco vertical]
[Termos sementes]
[Termos orgânicos descobertos]
[Indicadores econômicos relacionados]
[Score de associação]
```

### 9.5 Página 3 — Organic Terms Discovery

Objetivo:

Mostrar a parte mais original do projeto.

Componentes:

- tabela de termos orgânicos;
- ranking de rising/breakout terms;
- gráfico por categoria;
- rede termo semente → termo orgânico.

Exemplo de rede:

```text
Petrobras → gasolina hoje
Petrobras → dividendos
gasolina → ICMS gasolina
gasolina → preço gasolina
```

### 9.6 Página 4 — Before & After

Objetivo:

Comparar períodos anteriores e posteriores ao evento.

Filtros:

```text
Evento
Termo
Indicador econômico
Janela: 30 / 90 / 180 / 365 dias
```

Métricas:

- média antes;
- média depois;
- variação percentual;
- pico;
- duração;
- meia-vida;
- delay até pico.

### 9.7 Página 5 — Economic Impact

Objetivo:

Analisar o impacto econômico associado aos eventos.

Indicadores:

- gasolina;
- inflação;
- câmbio;
- juros;
- desemprego;
- bolsa;
- PIB;
- salário real.

Visualizações:

- linha temporal;
- barras antes/depois;
- dispersão entre pico de busca e variação econômica;
- ranking de eventos por choque econômico.

### 9.8 Página 6 — Cross-Country Comparison

Objetivo:

Comparar países corretamente usando métricas normalizadas.

Visualizações:

- Event Spike Ratio por país;
- duração da repercussão;
- volatilidade;
- categoria dominante;
- variação econômica;
- resposta a eventos equivalentes.

Nunca comparar volume bruto de busca.

Comparar sempre:

```text
baseline interno
pico relativo
duração
volatilidade
share por categoria
delay até pico
```

### 9.9 Página 7 — US Influence Layer

Objetivo:

Analisar influência de eventos dos EUA sobre Brasil e Argentina.

Fluxo visual:

```text
Evento nos EUA
↓
Indicador global
↓
Resposta Brasil
↓
Resposta Argentina
```

Indicadores:

- Fed Funds Rate;
- DXY;
- petróleo;
- S&P 500;
- inflação EUA;
- juros EUA.

Métricas:

- Lag Response;
- External Influence Score;
- variação cambial;
- variação inflação;
- pico de busca local.

### 9.10 Página 8 — Methodology Lab

Objetivo:

Aumentar confiança e transparência.

Conteúdo:

- como os dados foram coletados;
- como o Google Trends normaliza dados;
- diferença entre atenção pública e opinião pública;
- diferença entre correlação e causalidade;
- como os termos orgânicos foram descobertos;
- como os scores foram calculados;
- como os países foram comparados;
- limitações do projeto;
- fontes usadas.

### 9.11 Página 9 — Data Explorer

Objetivo:

Permitir inspecionar os dados brutos e tratados.

Componentes:

- tabela de eventos;
- tabela de termos orgânicos;
- tabela de indicadores econômicos;
- filtros por país, evento, fonte e categoria;
- opção de download CSV.

Isso aumenta transparência.

---

## 10. Estrutura de dados adicional

### 10.1 Tabela `country_baselines`

| Campo | Descrição |
|---|---|
| country | país |
| term | termo |
| event_id | evento |
| baseline_window | janela pré-evento |
| baseline_mean | média pré-evento |
| baseline_std | desvio padrão pré-evento |
| baseline_min | mínimo pré-evento |
| baseline_max | máximo pré-evento |

### 10.2 Tabela `normalized_metrics`

| Campo | Descrição |
|---|---|
| event_id | evento |
| country | país |
| term | termo |
| peak_value | valor do pico |
| spike_ratio | pico / média pré-evento |
| abnormal_interest_pct | interesse anormal percentual |
| duration_days | duração da repercussão |
| half_life_days | meia-vida do interesse |
| delay_to_peak_days | dias até o pico |
| volatility_score | volatilidade da série |

### 10.3 Tabela `external_shocks`

| Campo | Descrição |
|---|---|
| shock_id | identificador do choque externo |
| date | data |
| source_country | país de origem |
| shock_name | nome do evento |
| shock_type | tipo do choque |
| global_indicator | indicador global relacionado |
| description | descrição |

### 10.4 Tabela `external_influence_metrics`

| Campo | Descrição |
|---|---|
| shock_id | choque externo |
| affected_country | país afetado |
| local_term | termo local |
| local_indicator | indicador local |
| lag_response_days | delay até pico |
| local_spike_ratio | spike ratio local |
| economic_variation_pct | variação econômica local |
| external_influence_score | score de influência externa |

---

## 11. Roadmap atualizado sem pivotar

### Fase 1 — MVP Brasil

Manter como planejado:

- eventos domésticos do Brasil;
- termos orgânicos;
- Google Trends;
- indicadores econômicos;
- Streamlit inicial.

Não começar com tudo global.

### Fase 2 — Adicionar normalização

Implementar:

- baseline pré-evento;
- Event Spike Ratio;
- Abnormal Interest Index;
- duração;
- meia-vida;
- delay até pico;
- Association Confidence Score.

### Fase 3 — Expandir para EUA e Argentina

Adicionar eventos domésticos equivalentes:

- eleições;
- inflação;
- combustíveis;
- crises institucionais;
- reformas econômicas.

### Fase 4 — Comparação internacional

Criar página:

- Cross-Country Comparison.

Comparar apenas métricas normalizadas.

### Fase 5 — Adicionar influência dos EUA

Criar módulo:

- US Shock → Latin America Response.

Eventos iniciais:

```text
alta de juros do Fed
eleição presidencial americana
choque do petróleo
inflação americana
guerra comercial EUA-China
```

### Fase 6 — Melhorar UX

Adicionar:

- home executiva;
- event explorer;
- organic terms discovery;
- before & after;
- cross-country comparison;
- US influence layer;
- methodology lab;
- data explorer.

---

## 12. Princípios finais do projeto

### Princípio 1 — Não comparar volume bruto entre países

Comparar apenas métricas normalizadas.

### Princípio 2 — Não afirmar causalidade forte

Usar linguagem de associação temporal.

### Princípio 3 — Eventos primeiro, termos depois

Manter a lógica original:

```text
evento → termos orgânicos → indicadores → análise
```

### Princípio 4 — Mostrar score de confiança

Nem toda associação é forte.

### Princípio 5 — Separar doméstico de externo

Distinguir:

- evento interno;
- decisão política;
- crise institucional;
- choque externo;
- influência dos EUA.

### Princípio 6 — UX de investigação

O app deve permitir explorar, comparar, filtrar e entender.

Não deve parecer só um dashboard estático.

---

## 13. Resumo executivo

Este complemento reforça que o projeto está no caminho certo e não precisa ser pivotado.

A proposta final fica:

> Um estudo aplicado e interativo sobre como eventos políticos, decisões econômicas e choques externos geram repercussão orgânica em buscas públicas, como essa repercussão se manifesta em diferentes países e como ela se relaciona com indicadores econômicos.

A estrutura final deve combinar:

```text
Repercussão doméstica
+ Impacto econômico
+ Comparação internacional normalizada
+ Influência dos EUA na América Latina
+ UX investigativa em Streamlit
+ Metodologia transparente
```

Com isso, o projeto fica mais robusto, mais sério e mais interessante como estudo aplicado.
