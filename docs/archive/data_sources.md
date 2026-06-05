# Fontes de dados

Este arquivo organiza as fontes por papel no projeto. A ideia e separar:

- fontes comparaveis entre paises;
- fontes especificas de cada pais;
- fontes planejadas, mas ainda nao conectadas.

## Camada comparavel internacional

### World Bank API

Status: conectada.

Uso:

- Brasil;
- Estados Unidos;
- Argentina.

Indicadores coletados:

- inflacao anual;
- desemprego;
- crescimento anual do PIB;
- PIB per capita;
- divida do governo central, quando disponivel.

Observacao:

O World Bank e bom para comparacao internacional, mas a granularidade e anual. Ele nao substitui dados mensais/diarios em analises de curto prazo.

## Brasil

### Banco Central do Brasil - SGS

Status: conectado.

Indicadores coletados:

- IPCA, SGS 433;
- Selic, SGS 11;
- taxa de cambio, SGS 1;
- gasolina, SGS 24369.

Uso:

Base principal de indicadores economicos brasileiros para analises de curto, medio e longo prazo.

## Estados Unidos

### FRED

Status: conectado.

Indicadores coletados:

- CPI;
- Effective Federal Funds Rate;
- Unemployment Rate;
- US Regular Gas Price;
- Real GDP.

Observacao:

S&P 500 foi considerado, mas ficou fora da primeira versao porque o endpoint CSV estava instavel/lento. Pode voltar depois por FRED ou outra fonte.

## Argentina

### World Bank API

Status: conectada.

Uso:

Camada comparavel anual para inflacao, desemprego, PIB e indicadores macro.

### Bluelytics

Status: conectada.

Uso:

- dolar oficial;
- dolar blue;
- evolucao cambial argentina.

Observacao:

Os dados historicos diarios sao coletados em `scripts/collect_bluelytics.py`, salvos em `data/raw/bluelytics_evolution.csv` e consolidados em `data/processed/bluelytics_indicators_argentina.csv`.
Essas series desbloqueiam a leitura de curto prazo da Argentina para eventos com data exata ou mes aproximado.

## Fontes futuras

- GDELT GKG tone, para tom de cobertura midiatico;
- Google Trends / pytrends, para atencao publica e termos relacionados;
- IMF, para indicadores macro internacionais;
- Gallup e Latinobarometro, para percepcao social e opiniao publica.
