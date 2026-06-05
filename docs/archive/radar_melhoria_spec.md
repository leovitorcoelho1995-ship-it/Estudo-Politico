# Radar Político-Econômico — Spec de Melhorias

> Nota de manutencao: este documento e historico. Consulte `docs/project_memory.md` e `docs/post_report_update.md` para o estado atual do app. Varias melhorias aqui ja foram implementadas ou substituidas por solucoes mais recentes.


Documento de referência para passar a uma LLM ou IDE e executar as melhorias em sequência.
Cada bloco é independente e pode ser implementado em ordem ou separado.

---

## Contexto do projeto atual

- `app.py` — Streamlit com ~1258 linhas
- Views: `country_view`, `comparison_view`, `methodology_view`
- Navegação: 3 radio buttons no topo (o que ver / nível de detalhe / país)
- Dados carregados via `load_data()` com `@st.cache_data`
- Identidade visual: fundo papel `#f5f2ed`, verde `#0d7a5f`, tipografia DM Serif + Syne + DM Mono
- Stack de dados: BCB SGS (BR), FRED (USA), World Bank API (BR/USA/ARG)
- Lacuna conhecida: Google Trends ainda não integrado; Argentina sem dados frequentes

---

## Bloco 1 — Navegação e estrutura geral

### Problema
Os três radio buttons no topo (o que ver / nível de detalhe / país) ficam em linha e criam confusão de hierarquia. O usuário não sabe qual controla o quê.

### O que fazer

Substituir os radio buttons soltos por um layout de navegação com dois níveis claros:

**Nível 1 — sidebar fixa (esquerda):**
```
[ Brasil ]  [ Estados Unidos ]  [ Argentina ]  [ Comparar países ]  [ Metodologia ]
```
Usar `st.sidebar` com botões estilizados ou `st.radio` vertical na sidebar com CSS customizado.

**Nível 2 — toggle dentro do conteúdo:**
No canto superior direito de cada view, um toggle discreto:
```
[ leitura simples ]  [ modo técnico ]  [ meu aprendizado ]
```

### Resultado esperado
- Sidebar com país/modo selecionado visualmente destacado
- Toggle de detalhe separado e contextual, não misturado com a seleção de país
- Terceira opção "meu aprendizado" (ver Bloco 5)

---

## Bloco 2 — Interatividade evento → gráfico

### Problema atual
O evento é selecionado via `st.selectbox` separado da tabela. O usuário precisa:
1. ver a tabela
2. lembrar o nome do evento
3. ir até o selectbox e selecionar manualmente

Não há feedback visual imediato entre clicar num evento e ver o efeito no gráfico.

### O que fazer

**Passo 1 — substituir selectbox por tabela clicável:**

Usar `st.dataframe` com `on_select="rerun"` e `selection_mode="single-row"` (disponível no Streamlit ≥ 1.35):

```python
selected = st.dataframe(
    event_table(country_events),
    use_container_width=True,
    hide_index=True,
    height=360,
    on_select="rerun",
    selection_mode="single-row",
)
if selected["selection"]["rows"]:
    row_idx = selected["selection"]["rows"][0]
    selected_event_id = country_events.iloc[row_idx]["event_id"]
else:
    selected_event_id = country_events.iloc[0]["event_id"]
```

**Passo 2 — scroll automático para o gráfico:**

Após a seleção, usar `st.markdown` com âncora HTML para rolar até a seção do gráfico:
```python
st.markdown('<div id="grafico-indicadores"></div>', unsafe_allow_html=True)
```
E injetar JS via `st.components.v1.html` para forçar scroll quando o evento mudar.

**Passo 3 — callout de confirmação visual:**

Quando um evento é selecionado pela tabela, mostrar um callout antes do gráfico:
```
📍 Você selecionou: "Teto ICMS combustíveis" · jun/2022 · Fiscal
A linha vermelha no gráfico marca quando esse evento aconteceu.
```

**Passo 4 — coluna visual na tabela:**

Adicionar coluna `impacto` na tabela de eventos com badge colorido:
- `alto` (verde escuro) se `abs_standardized_change > 1.5`
- `médio` (âmbar) se entre 0.5 e 1.5
- `baixo` (cinza) se < 0.5
- `sem dados` (cinza claro) se Argentina ou sem curto prazo

```python
def classify_impact(event_id, short_rank):
    row = short_rank[short_rank["event_id"] == event_id]
    if row.empty:
        return "sem dados"
    val = row["abs_standardized_change"].max()
    if val > 1.5:
        return "alto"
    elif val > 0.5:
        return "médio"
    return "baixo"
```

---

## Bloco 3 — Visualização evento × movimento

### Problema atual
O gráfico de série temporal (z-score) e o gráfico de barras de impacto (antes/depois) estão separados em seções 03 e 04, sem conexão visual clara entre eles.

### O que fazer

**Layout de duas colunas lado a lado para o par evento/impacto:**

```
[ Série temporal com evento marcado ] | [ Barras antes/depois do evento ]
          col 70%                     |          col 30%
```

Usar `st.columns([2.3, 1])`.

Na coluna da esquerda: gráfico de linha com z-score e evento destacado em vermelho.

Na coluna da direita:
- Nome do evento em destaque
- Data do evento
- Mini barras horizontais mostrando os 3 indicadores com maior movimento
- Seta indicando direção (↑ subiu / ↓ caiu)
- Magnitude em desvios-padrão

Exemplo de mini-card lateral:
```
Gasolina          ↑ 2,3σ  ████████░░
Câmbio            ↑ 1,8σ  ██████░░░░
Inflação (IPCA)   ↑ 1,2σ  ████░░░░░░
```

Esse lado direito pode ser HTML puro via `st.markdown` com `unsafe_allow_html=True`.

---

## Bloco 4 — Cobertura e período dos dados

### Problema atual
- "Trajetórias anuais comparáveis" (World Bank) vai até 2024 apenas
- O projeto cobre 2016–2026 mas os dados anuais do World Bank atrasam ~1–2 anos
- A cobertura inconsistente entre fontes não está explicada para o usuário

### O que fazer

**Passo 1 — documentar o atraso do World Bank no próprio app:**

Adicionar `plain_note` nas seções que usam World Bank:
```
"Dados anuais do World Bank chegam com atraso de 1–2 anos. 
A cobertura efetiva desta análise vai de 2016 a 2024."
```

**Passo 2 — ajustar o período declarado:**

No hero/header, mudar de `2016-2026` para `2016-2024 (anual) · 2016-2026 (diário/mensal)`.

**Passo 3 — adicionar tabela de cobertura por fonte no modo técnico:**

| Fonte | País | Frequência | Início | Fim real |
|---|---|---|---|---|
| BCB SGS | Brasil | diária/mensal | jan/2016 | jun/2026 |
| FRED | EUA | semanal/mensal/trim. | jan/2016 | jun/2026 |
| World Bank | BR/USA/ARG | anual | 2016 | 2024 |

Essa tabela já existe parcialmente em `methodology_view` — expandir e mover para a view de cada país no modo técnico.

**Passo 4 — no script `collect_world_bank.py`:**

Adicionar parâmetro `mrv=10` na chamada da API para garantir que os 10 anos mais recentes disponíveis são sempre coletados, não apenas os últimos 5.

---

## Bloco 5 — Modo "meu aprendizado" (visão escondida para o autor)

### Objetivo
Uma terceira camada de visualização além de "leitura simples" e "modo técnico": uma visão pedagógica que explica o que foi feito em cada seção, por que foi feito assim, e como replicar do zero.

### Como implementar

**Toggle:**
```python
explanation_mode = st.radio(
    "nível de detalhe",
    ["leitura simples", "modo técnico", "meu aprendizado"],
    horizontal=True,
)
learning_mode = explanation_mode == "meu aprendizado"
```

**Padrão de uso em cada seção:**

Criar função `learning_expander(title, what, why, how_to_replicate, code)`:

```python
def learning_expander(title, what, why, replicate, code, enabled):
    if not enabled:
        return
    with st.expander(f"📘 {title}", expanded=True):
        st.markdown("**O que está acontecendo aqui:**")
        st.write(what)
        st.markdown("**Por que essa decisão foi tomada:**")
        st.write(why)
        st.markdown("**Como replicar do zero:**")
        st.write(replicate)
        st.code(code.strip(), language="python")
```

**Conteúdo por seção:**

| Seção | O que explicar |
|---|---|
| KPI cards | Contagem de eventos/países/registros — como esses números são gerados |
| Série z-score | O que é z-score, por que normalizar, como calcular com pandas |
| Evento no gráfico | Como `add_shape` e `add_annotation` funcionam no Plotly |
| Barras antes/depois | Como o motor de impacto calcula média antes/depois por janela |
| Rankings | Como o ranking é montado e ordenado por `abs_standardized_change` |
| Comparação entre países | Por que z-score e não valor bruto; limitações da comparação |
| Trajetórias anuais | O que é `z_change_from_previous_year` e como interpretar |

**Exemplo de conteúdo para a seção z-score:**

```
O QUE ESTÁ ACONTECENDO:
O gráfico não mostra o valor original do indicador (ex: IPCA = 12,13%).
Mostra o z-score: o quanto esse valor está distante da média histórica daquele país.

POR QUE:
Se você colocar a inflação do Brasil (12%) e a dos EUA (8%) no mesmo gráfico,
parece que o Brasil teve pouco impacto e os EUA tiveram muito.
Mas se a inflação normal do Brasil é 6% e a dos EUA é 2%, o choque relativo
foi parecido. O z-score corrige isso.

COMO REPLICAR:
1. Calcule a média e desvio padrão histórico por país + indicador
2. Para cada observação: z = (valor - media) / desvio_padrao
3. Plote z no lugar do valor original

CÓDIGO:
df["z_score"] = df.groupby(["country_code","indicator_slug"])["value"].transform(
    lambda x: (x - x.mean()) / x.std()
)
```

---

## Bloco 6 — Google Trends (nova camada de dados)

### Objetivo
Adicionar a camada de atenção pública via `pytrends`, cruzando picos de busca com eventos políticos.

### Scripts novos a criar

**`scripts/collect_trends.py`:**

```python
import time
import pandas as pd
from pytrends.request import TrendReq

EVENTS = pd.read_csv("data/raw/political_events.csv")

SEED_TERMS = {
    # Brasil
    "BR_2022_ICMS":       ["gasolina", "preço combustível", "ICMS gasolina"],
    "BR_2020_AUXILIO":    ["auxílio emergencial", "coronavírus auxílio"],
    "BR_2023_8JAN":       ["8 de janeiro", "brasília invasão"],
    "BR_2018_GREVE_CAM":  ["greve caminhoneiros", "diesel greve"],
    # USA
    "US_2021_STIMULUS":   ["stimulus check", "Biden check"],
    "US_2022_INFLATION":  ["inflation 2022", "gas price USA"],
    # ARG — termos em espanhol
    "AR_2018_FMI":        ["dólar blue", "FMI Argentina"],
    "AR_2023_MILEI":      ["Milei", "dolarización Argentina"],
}

GEO_MAP = {"BR": "BR", "US": "US", "AR": "AR"}

def collect_for_event(event_key, terms, geo, timeframe):
    pt = TrendReq(hl="pt-BR", tz=-180)
    pt.build_payload(terms[:5], geo=geo, timeframe=timeframe)
    time.sleep(2)  # evitar rate limit
    interest = pt.interest_over_time()
    if interest.empty:
        return None, None
    related = pt.related_queries()
    return interest, related

# Loop principal — salvar em data/raw/trends_{event_key}.csv
```

**`scripts/build_trends_layer.py`:**

```python
# Lê todos os CSVs de trends
# Normaliza para z-score da própria série
# Salva em data/processed/trends_normalized.csv
# Colunas: event_key, country_code, date, term, interest, z_score
```

**`scripts/build_trends_event_alignment.py`:**

```python
# Para cada evento, calcula:
# - pico de busca mais próximo ao evento (em dias)
# - se o pico veio ANTES ou DEPOIS do evento
# - intensidade do pico (z-score)
# Salva em data/processed/trends_event_alignment.csv
```

### Como integrar no app

Nova seção `03b` dentro de `country_view`, entre a série z-score e o gráfico de impacto:

```python
section_header("03b", "Atenção pública ao redor do evento", "atenção")
plain_note(
    "O Google Trends mede o interesse de busca relativo. "
    "Aqui ele aparece junto com os indicadores econômicos para mostrar "
    "quando o público percebeu o evento — antes ou depois dos números mudarem."
)
```

Gráfico: linha de Trends sobreposta à linha de z-score do indicador mais relacionado, com o evento marcado.

---

## Bloco 7 — Argentina: indicadores frequentes

### Problema
Argentina tem 12 eventos mas zero no motor de curto prazo porque só tem dados anuais (World Bank).

### Scripts novos a criar

**`scripts/collect_bluelytics.py`:**
```python
import requests, pandas as pd

url = "https://api.bluelytics.com.ar/v2/evolution.json"
resp = requests.get(url)
df = pd.DataFrame(resp.json())
# colunas: date, source_name, value_buy, value_sell
df = df[df["source_name"] == "Blue"]
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"] >= "2016-01-01"]
df.to_csv("data/raw/arg_dolar_blue.csv", index=False)
```

Após coleta, incluir no pipeline de normalização (`build_normalized_economic_indicators.py`) com `country_code=ARG`, `indicator_slug=dolar_blue`, `frequency=daily`.

---

## Bloco 8 — Correções de código

### Bug: `fiscal_social` duplicado em `SUBCATEGORY_LABELS`

No `app.py`, linha ~89, há chave duplicada:
```python
# linha 76
"fiscal_social": "Gasto publico e renda",
# linha 89 — sobrescreve silenciosamente
"fiscal_social": "Fiscal e social",
```
Corrigir: escolher um label definitivo ou criar chaves distintas (`fiscal_social_br` vs `fiscal_social_ar`).

### Melhoria: `story_callout` e `plain_note` sem escape HTML

Funções atuais:
```python
def story_callout(text: str) -> None:
    st.markdown(f'<div class="story-callout">{text}</div>', unsafe_allow_html=True)
```
Adicionar `html.escape(text)` no conteúdo dinâmico que pode conter dados brutos.

### Melhoria: `section_header` com replace frágil

Função atual usa `title.replace(emphasis, f"<em>{emphasis}</em>")` — substitui todas as ocorrências.
Substituir por replace com `count=1`:
```python
title_html = title.replace(emphasis, f"<em>{emphasis}</em>", 1)
```

---

## Bloco 9 — Conteúdo para LinkedIn (prints do app)

### Quais telas geram prints interessantes

| Tela | Por que funciona no LinkedIn |
|---|---|
| Hero + KPI cards (4 números) | Projeto de dados real com escala: 43 eventos, 3 países, 6,5k registros |
| Gráfico z-score BR com evento marcado (ex: ICMS jun/2022) | Conta uma história clara: linha sobe, evento marcado, interpretação |
| Barras antes/depois de um evento específico | Muito visual, intuitivo mesmo sem contexto técnico |
| Comparação de trajetórias anuais (3 países, pandemia visível) | Mostra habilidade de análise comparativa |

### O que NÃO postar

- Nomes de presidentes ou partidos em destaque
- Qualquer recorte que pareça endossar ou criticar um lado
- Rankings com linguagem valorativa ("pior evento", "maior destruição")

### Texto sugerido para post (neutro)

```
Projeto de análise: como eventos políticos se relacionam com indicadores econômicos.

Construí um pipeline completo de dados públicos (BCB, FRED, World Bank) 
cobrindo Brasil, EUA e Argentina de 2016 a 2026.

A métrica principal não é o valor bruto — é o z-score: 
o quanto o indicador saiu do próprio padrão histórico do país.

Isso permite comparar choques de economias completamente diferentes.

Stack: Python · Pandas · Plotly · Streamlit
Fontes: BCB SGS · FRED · World Bank API

[print do gráfico z-score com evento marcado]
```

---

## Ordem de execução recomendada

| Prioridade | Bloco | Esforço estimado | Impacto |
|---|---|---|---|
| 1 | Bloco 8 — bugs e correções | 30 min | baixo esforço, elimina riscos |
| 2 | Bloco 2 — tabela clicável → gráfico | 2h | maior mudança de UX |
| 3 | Bloco 3 — layout evento × movimento | 2h | mais impacto visual |
| 4 | Bloco 1 — sidebar de navegação | 3h | elimina confusão de controles |
| 5 | Bloco 5 — modo aprendizado | 3h | valor pessoal alto |
| 6 | Bloco 4 — cobertura e período | 1h | clareza metodológica |
| 7 | Bloco 7 — Argentina Bluelytics | 2h | fecha lacuna do motor |
| 8 | Bloco 6 — Google Trends | 4h | adiciona camada nova |
| 9 | Bloco 9 — LinkedIn | após telas prontas | visibilidade |

---

## Prompt pronto para passar à LLM/IDE

```
Você vai trabalhar no arquivo app.py de um projeto Streamlit chamado 
"Radar Político-Econômico". O app analisa como eventos políticos 
se relacionam com indicadores econômicos no Brasil, EUA e Argentina.

Contexto técnico:
- ~1258 linhas de Python
- Views: country_view, comparison_view, methodology_view
- Dados via load_data() com @st.cache_data
- Identidade visual: fundo #f5f2ed, verde #0d7a5f, DM Serif + Syne + DM Mono

Implemente a seguinte melhoria: [DESCREVA O BLOCO AQUI]

Regras:
1. Não altere a identidade visual existente
2. Não remova nenhuma seção existente, apenas refatore
3. Mantenha o padrão de funções auxiliares (plain_note, story_callout, section_header)
4. Adicione comentários explicando o que cada bloco novo faz
5. Se criar novos scripts de coleta, salve em scripts/ e processe em data/processed/
```
