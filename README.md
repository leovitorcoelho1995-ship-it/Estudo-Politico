# Radar Politico-Economico

Aplicacao analitica para estudar como eventos politico-economicos se relacionam com movimentos em indicadores economicos, atencao publica e rankings de choque.

O relatorio atual e completo do projeto esta em:

```text
docs/project_status_report.md
```

## Como rodar

No PowerShell, dentro da pasta do projeto:

```powershell
python scripts/run_pipeline.py
```

Para refazer tambem as coletas externas:

```powershell
python scripts/run_pipeline.py --with-collection
```

Se quiser pular os graficos HTML exploratorios:

```powershell
python scripts/run_pipeline.py --skip-charts
```

## App Streamlit

Para rodar:

```powershell
python -m streamlit run app.py
```

## Estado resumido

| Item | Estado |
| --- | --- |
| Eventos | 88 totais; 79 com curto prazo |
| Paises | Brasil, Estados Unidos, Argentina |
| Score | `score_v1_1_trends_partial` |
| Fontes | top 15 com URL; demais contextuais |
| Trends | parcial; limitado por 429 do Google |
| App | funcional em Streamlit |
| Relatorio completo | `docs/project_status_report.md` |
