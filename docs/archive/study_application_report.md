# Relatorio do estudo e da aplicacao

> Nota de manutencao: este relatorio registra uma fotografia anterior do projeto. As implementacoes feitas depois dele estao em `docs/post_report_update.md`.


## Resumo executivo

O projeto esta em um nivel forte de prototipo analitico: ja possui pipeline multi-pais, normalizacao, eventos com volume adequado, app Streamlit funcional, leitura por pais, comparacao internacional, Google Trends inicial, robustez historica, significancia, contaminacao por eventos proximos, persistencia do choque e event study individual/agregado.

O principal ganho recente foi sair de uma base subdimensionada para 88 eventos totais, com 79 eventos com cobertura de curto prazo:

| Pais | Eventos totais | Eventos curto prazo | Situacao |
| --- | ---: | ---: | --- |
| Argentina | 25 | 20 | dentro do minimo |
| Brasil | 34 | 32 | dentro do alvo |
| Estados Unidos | 29 | 27 | dentro do alvo |
| Projeto | 88 | 79 | base analitica mais defensavel |

A aplicacao esta coerente para demonstracao e exploracao. Para ficar mais proxima de um produto analitico/academico robusto, os pontos mais importantes agora sao: documentar melhor vies de selecao de eventos, consolidar um score final explicavel, melhorar a comparacao entre paises para incluir tambem curvas agregadas de curto prazo, e expandir/atualizar Google Trends para os eventos novos.

## Estrutura logica

O fluxo atual e coerente:

1. coleta de series economicas;
2. unificacao das bases;
3. normalizacao por pais e indicador;
4. catalogo de eventos;
5. calculo de antes/depois;
6. significancia estatistica;
7. robustez historica;
8. contaminacao por eventos proximos;
9. persistencia do choque;
10. event study individual;
11. curvas agregadas por categoria;
12. rankings e dashboard.

Essa ordem faz sentido porque evita comparar valores brutos entre economias diferentes e separa varias perguntas que normalmente ficam misturadas:

- tamanho do movimento;
- raridade historica;
- significancia estatistica;
- persistencia;
- contaminacao por eventos proximos;
- atencao publica.

## Qualidade metodologica

### Pontos fortes

- Normalizacao por z-score e base 100 evita comparacoes brutas enganosas entre Brasil, EUA e Argentina.
- Separacao entre dados frequentes e dados anuais do World Bank esta correta.
- Eventos longos (`year`, `year_range`) ficam fora do curto prazo, o que evita tratar periodos amplos como choque pontual.
- A auditoria automatica deixa lacunas visiveis.
- A expansao para 88 eventos permite subgrupos por pais/categoria com N mais informativo.
- O projeto diferencia associacao temporal de causalidade.
- A camada de contaminacao ajuda a reduzir leitura causal indevida.
- Persistencia e event study melhoram a narrativa: nao e so "mexeu", mas tambem "quando", "quanto tempo" e "se voltou ao normal".

### Pontos fracos

- A selecao de eventos ainda depende de curadoria manual. Existe criterio, mas ainda faltam fontes/links por evento.
- Google Trends cobre apenas parte dos eventos, sobretudo antes da expansao recente.
- Significancia atual e util como triagem, mas ainda nao substitui desenho causal.
- Eventos muito proximos aumentaram bastante; isso melhora cobertura, mas tambem aumenta contaminacao de janelas.
- USA tem varias series mensais/semanal/trimestral; em alguns event studies agregados, o N por dia relativo fica baixo.
- Argentina tem so dois indicadores frequentes, ambos cambiais; isso torna o curto prazo muito sensivel a cambio e menos amplo macroeconomicamente.
- Ainda nao ha controle explicito por tendencia, sazonalidade, dummies de ano ou regime macro.

## Robustez

O projeto ja tem quatro camadas relevantes de robustez:

- robustez historica por percentil;
- significancia com p-value/FDR;
- contaminacao por eventos proximos;
- persistencia/event study.

Isso e forte para um estudo exploratorio. O limite e que essas camadas ainda medem padroes temporais, nao causalidade identificada. A leitura correta e:

> "este evento coincide com movimento raro/significativo/persistente em indicadores", nao "este evento causou o movimento".

Ponto de atencao: ha alta contaminacao em janelas de 90/180 dias em varios paises, especialmente depois da expansao. Isso deve aparecer mais forte no storytelling e nos rankings.

## Aplicacao Streamlit

### Estrutura de UX

A aplicacao tem boa arquitetura de navegacao:

- `Pais por pais`;
- `Comparar paises`;
- `Metodologia`;
- pais selecionavel quando aplicavel;
- nivel de detalhe: `Simples`, `Tecnico`, `Meu aprendizado`.

O topo funciona bem como cockpit. KPIs iniciais dao escala do projeto. A tabela clicavel de eventos cria uma interacao clara: selecionar evento -> graficos abaixo mudam.

### Modo simples

Funciona. Ele prioriza narrativa, graficos e notas curtas. E o modo mais adequado para portfolio/demonstracao.

Melhoria recomendada:

- reduzir densidade em algumas secoes do pais, porque ja ha muitas leituras: linha do tempo, indicadores, Trends, movimento, event study individual, curva agregada, ranking, anual.
- considerar abas internas dentro do pais: `Evento`, `Padroes`, `Rankings`, `Anual`.

### Modo tecnico

Funciona. Os expanders tecnicos aparecem e explicam arquivos, formulas e logica.

Melhoria recomendada:

- incluir nos expanders tecnicos as novas camadas recentes: contaminacao, persistencia e curva agregada por categoria.
- explicitar o limite dos p-values: teste antes/depois nao equivale a desenho causal.
- mostrar caminho dos arquivos usados em cada secao.

### Modo meu aprendizado

Funciona. Os blocos pedagogicos aparecem abertos e explicam o raciocinio.

Melhoria recomendada:

- completar blocos de aprendizado para as novas secoes: persistencia, event study e curva agregada.
- hoje ele e bom para KPIs, normalizacao e comparacao anual; ainda nao cobre todo o pipeline novo.

## Relacao entre paises

A logica atual de comparacao entre paises e correta: usa z-score e dados anuais comparaveis do World Bank, evitando valores brutos.

Ponto forte:

- a comparacao anual e metodologicamente mais justa entre paises.

Limite:

- a tela `Comparar paises` ainda depende demais do World Bank anual.
- agora que ha event study agregado, faz sentido adicionar uma comparacao multi-pais de curto prazo por categoria, por exemplo:
  - economia no Brasil vs economia nos EUA vs economia na Argentina;
  - politica no Brasil vs politica nos EUA vs politica na Argentina;
  - curva media por pais para a mesma categoria.

Isso conectaria melhor a expansao de eventos com a visao internacional.

## Dados e cobertura

### Fortes

- Brasil: boa cobertura frequente para cambio, Selic, IPCA e gasolina.
- EUA: boa cobertura, mas com frequencias mistas.
- Argentina: cobertura diaria forte para dolar oficial e blue.
- World Bank cria base anual comparavel.

### Fracos

- Argentina precisa de inflacao mensal, taxa de juros, risco pais ou combustiveis para sair do eixo quase exclusivamente cambial.
- Trends precisa ser reprocessado/expandido para eventos novos.
- USA poderia ganhar series diarias/financeiras para eventos Fed/bancos, por exemplo yield 10y, VIX, DXY ou S&P 500, se o objetivo aceitar indicadores financeiros.

## Pontos fortes gerais

- Escopo claro.
- Pipeline modular.
- App navegavel e funcional.
- Boa separacao entre leitura simples, tecnica e pedagogica.
- Aumento de N deixou o estudo mais defensavel.
- Auditoria automatica evita esconder lacunas.
- Metodologia de normalizacao e adequada.
- A narrativa ja evita causalidade exagerada.

## Pontos fracos gerais

- Falta um `run_pipeline.py` unico.
- Dicionarios de labels e logica de UX ainda estao concentrados no `app.py`.
- Algumas documentacoes de backlog ficaram desatualizadas, ainda listando como pendente algo que ja foi implementado.
- Falta fonte individual por evento alem de `source_note` generico.
- Falta score final sintetico e explicavel.
- Google Trends ficou atrasado em relacao a expansao de eventos.
- Rankings ainda precisam integrar melhor robustez, significancia, persistencia e contaminacao em uma unica leitura.

## Recomendacoes prioritarias

1. Criar `event_final_score.csv`.
   - Combinar impacto, robustez, significancia, persistencia, Trends e penalidade por contaminacao.

2. Expandir Google Trends para os 88 eventos.
   - Pelo menos 1-3 termos por evento.
   - Marcar eventos sem termo confiavel.

3. Adicionar comparacao multi-pais de curto prazo.
   - Curva agregada por categoria e pais.
   - Exemplo: `economy`: ARG vs BRA vs USA.

4. Criar `run_pipeline.py`.
   - Evita rodar 15 scripts manualmente.

5. Atualizar metodologia no app.
   - Incluir criterios de selecao de eventos.
   - Explicar eventos longos.
   - Explicar contaminacao.
   - Explicar limites dos testes estatisticos.

6. Melhorar fontes dos eventos.
   - Adicionar coluna `source_url` ou arquivo auxiliar com fontes.

## Verificacao funcional

Verificacao local feita no app `http://127.0.0.1:8501`:

- app carregou;
- titulo renderizou corretamente;
- sem traceback;
- sem mojibake visivel no navegador;
- toggle `Simples` presente;
- toggle `Tecnico` funcional;
- toggle `Meu aprendizado` funcional;
- view `Comparar paises` funcional;
- secao de curva media por categoria presente.

## Conclusao

O projeto ja passa de prototipo de coleta para aplicacao analitica exploratoria consistente. A base de eventos agora tem volume suficiente para padroes por pais e categoria, especialmente em `economy`. A arquitetura metodologica e boa, mas ainda precisa consolidar a camada de sintese e atualizar Trends para acompanhar a expansao da base.

O proximo passo mais valioso e criar o score final de evento e uma tela de ranking explicavel. Isso transforma varias metricas soltas em uma leitura executiva clara, mantendo a capacidade tecnica de auditar cada componente.
