# Adendo — Tratamento do período World Bank

Complemento ao documento `radar_melhoria_spec.md`, bloco 4.

---

## Decisão registrada

Não travar o projeto em 2024. Cada camada de dados mantém seu próprio período real:

| Camada | Fonte | Período real | O que fazer |
|---|---|---|---|
| Diária / mensal | BCB SGS, FRED | 2016–2026 | deixar rolar sem restrição |
| Anual comparativa | World Bank API | 2016–2024 | filtrar ≤ 2024 só nos gráficos anuais |

O header do app continua declarando `2016–2026` — está correto porque a base como um todo cobre até 2026.

---

## Mudanças no app.py

### 1. Filtro nos gráficos que usam World Bank

Nos dois lugares onde `source == "World Bank API"` é plotado, adicionar filtro antes do `px.line` ou `px.bar`:

```python
# Aplicar APENAS em gráficos de trajetória anual (World Bank)
# NÃO aplicar nas séries diárias/mensais de BCB e FRED

WORLD_BANK_MAX_YEAR = 2024

plot_df = indicators[
    (indicators["source"] == "World Bank API")
    & (indicators["indicator_slug"] == selected)
    & (indicators["date"].dt.year <= WORLD_BANK_MAX_YEAR)
]
```

Definir `WORLD_BANK_MAX_YEAR = 2024` como constante no topo do arquivo, junto com as outras constantes. Assim quando o World Bank publicar 2025, basta mudar um número.

### 2. Filtro na tabela de contexto macro anual

Em `country_view`, seção 06 ("Contexto macro anual"), o dataframe `country_annual` vem de `ranking_annual_impacts.csv` que é gerado pelo World Bank. Filtrar antes de exibir:

```python
country_annual = annual_rank[
    (annual_rank["country_code"] == country)
    & (annual_rank["event_year"] <= WORLD_BANK_MAX_YEAR)
].copy()
```

### 3. Filtro na view de comparação entre países

Em `comparison_view`, a tabela `annual_context` e o gráfico de trajetórias usam World Bank. Filtrar nos dois pontos:

```python
# Gráfico de trajetórias anuais comparáveis
plot_df = indicators[
    (indicators["source"] == "World Bank API")
    & (indicators["indicator_slug"] == selected)
    & (indicators["date"].dt.year <= WORLD_BANK_MAX_YEAR)
]

# Ranking de contexto macro entre países
top = annual_context[
    annual_context["event_year"] <= WORLD_BANK_MAX_YEAR
].head(25).copy()
```

### 4. Notas explicativas nos gráficos afetados

Adicionar `plain_note` imediatamente antes de cada gráfico que usa World Bank:

```python
plain_note(
    f"Dados anuais (World Bank) — cobertura até {WORLD_BANK_MAX_YEAR}. "
    "O Banco Mundial publica com atraso de 1–2 anos. "
    "Séries diárias e mensais (BCB, FRED) cobrem até 2026."
)
```

### 5. Ajuste no header

No bloco hero do `header()`, a linha atual:
```python
'<div class="hero-eyebrow">Análise política e economia · 2016-2026</div>'
```

Manter como está — `2016–2026` está correto para o projeto como um todo.

Adicionar uma segunda linha abaixo, menor, em monospace:
```python
'<div class="hero-eyebrow" style="margin-top:.3rem; opacity:.7;">'
'diário/mensal até jun/2026 · anual até 2024'
'</div>'
```

---

## Mudança no script collect_world_bank.py

Garantir que a coleta sempre busca os anos mais recentes disponíveis. Adicionar o parâmetro `mrv` (most recent values) na chamada da API:

```python
# Antes (coleta número fixo de registros sem garantia de recência)
params = {"format": "json", "per_page": 500}

# Depois (garante os 10 anos mais recentes disponíveis)
params = {"format": "json", "per_page": 500, "mrv": 10}
```

Isso faz com que quando o World Bank publicar os dados de 2025, a próxima coleta os traga automaticamente. Quando isso acontecer, atualizar `WORLD_BANK_MAX_YEAR` de `2024` para `2025`.

---

## O que NÃO fazer

- Não filtrar BCB nem FRED — essas séries vão até 2026 e devem continuar assim
- Não mudar o período declarado no header de `2016–2026`
- Não remover eventos de 2025/2026 da tabela de eventos políticos
- Não aplicar o filtro no motor de impacto de curto prazo — ele usa BCB/FRED, não World Bank
