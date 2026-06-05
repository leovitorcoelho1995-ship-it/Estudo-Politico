# Metodologia de normalizacao entre paises

Brasil, Estados Unidos e Argentina tem tamanhos, moedas, regimes economicos, inflacao historica e estruturas produtivas muito diferentes. Por isso, o projeto nao deve comparar valores brutos como se fossem equivalentes.

Exemplo ruim:

```text
Comparar Selic do Brasil diretamente com Fed Funds dos EUA e concluir qual pais sofreu mais.
```

Exemplo correto:

```text
Comparar quanto cada indicador se moveu em relacao ao seu proprio historico.
```

## Principio central

A comparacao internacional deve usar medidas relativas e padronizadas:

1. indice base 100;
2. variacao percentual;
3. z-score por pais e indicador;
4. tamanho de choque em desvios-padrao;
5. comparacao anual separada para fontes anuais, como World Bank.

## Tipos de comparacao

### 1. Nivel bruto

Uso:

- mostrar contexto local;
- explicar o indicador no pais;
- fazer leitura domestica.

Nao usar para:

- comparar diretamente paises diferentes.

Exemplo:

- cambio BRL/USD;
- gasolina no Brasil;
- CPI dos EUA;
- inflacao anual argentina.

### 2. Indice base 100

Transforma cada serie para uma escala comum:

```text
valor_indexado = valor / primeiro_valor_da_serie * 100
```

Uso:

- comparar trajetorias;
- ver qual serie cresceu mais desde o inicio do recorte;
- criar graficos internacionais mais intuitivos.

Limite:

- sensivel ao ponto inicial escolhido.

### 3. Variacao percentual

Mede a mudanca relativa entre dois pontos:

```text
variacao_percentual = (valor_depois - valor_antes) / abs(valor_antes) * 100
```

Uso:

- comparar movimentos relativos.

Limite:

- pode explodir quando o valor inicial esta perto de zero.

### 4. Z-score por pais e indicador

Mede quantos desvios-padrao um valor esta acima ou abaixo da media historica daquela propria serie:

```text
z_score = (valor - media_da_serie) / desvio_padrao_da_serie
```

Uso:

- comparar intensidade relativa entre paises;
- dizer se um indicador estava em nivel incomum para aquele pais;
- reduzir problema de escala.

Exemplo interpretativo:

```text
z_score = 2.0
```

Significa que o indicador esta dois desvios-padrao acima da media historica daquela serie.

### 5. Tamanho de choque do evento

Para eventos politicos, o projeto deve comparar a mudanca antes/depois com a volatilidade historica do proprio indicador:

```text
choque_padronizado = (media_depois - media_antes) / desvio_padrao_historico
```

Uso:

- comparar impacto relativo de eventos entre paises;
- evitar que indicadores com unidades diferentes dominem a analise;
- ranquear eventos por intensidade padronizada.

## Regra metodologica do projeto

O dashboard e as analises devem separar:

| Pergunta | Metrica principal |
| --- | --- |
| O que aconteceu dentro de um pais? | valor bruto e variacao |
| Qual pais teve movimento mais forte? | z-score e choque padronizado |
| Como trajetorias evoluiram desde 2016? | indice base 100 |
| Como comparar Argentina com Brasil e EUA usando World Bank? | series anuais normalizadas |
| Como comparar eventos de curto prazo? | apenas dados diarios, semanais, mensais ou trimestrais |

## Cuidados

- Nao afirmar causalidade direta.
- Nao comparar moedas, juros ou indices em nivel bruto como equivalentes.
- Sempre mostrar fonte e frequencia.
- Separar analise anual de analise de curto prazo.
- Tratar Argentina com cuidado enquanto nao houver fonte frequente conectada.
