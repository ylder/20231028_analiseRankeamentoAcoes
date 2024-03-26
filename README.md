## 1 Descrição do projeto

A partir dos dados disponibilizados pela `Status Invest`, este módulo Python simples oferece uma solução para o rankeamento de ações com base em indicadores financeiros específicos.

Utilizando as bibliotecas Pandas e NumPy para manipulação e análise de dados, as classes `Dados` e `Rankeamento` simplificam o processo de carregamento de dados a partir do arquivo CSV, aplicam uma tabela de esquema específica e realizam o rankeamento das ações com base em parâmetros configuráveis.

O método de avaliação aplicado foi `Matriz de decisão`, incide sobre alguns indicadores que comunicam a capacidade de geração de riqueza, crescimento e liquidez das empresas, as quais seus tickers a representam no mercado de capitais; dessa forma, a avaliação é apenas considerando dados contábeis e econômicos das organizações.

## 2 Ferramentas e técnicas utilizadas

- VS Code
- Python 3.10.9

## 3 Objetivos do autor

- Aplicar conceitos aprendidos na Pós Graduação da Conquer em Business Intelligence e Analytics.
- Explorar o uso de classes e métodos para organização e fluxo do código;

## 4 Classes

### Classe `Dados`

#### Descrição

A classe `Dados` é projetada para representar dados provenientes de um arquivo CSV, realizando a leitura, formatação e limpeza dos dados.

#### Métodos

- **`__init__(self, arquivo: str)`**: Construtor da classe, recebe o caminho do arquivo CSV como parâmetro.

- **`tabela_status_invest(self) -> pd.DataFrame`**: Lê o arquivo CSV, aplica um esquema predefinido de colunas (schema), renomeia as colunas e remove as linhas que contêm valores nulos, retornando um DataFrame Pandas com os dados formatados.

### Classe `Rankeamento`

#### Descrição

A classe `Rankeamento` realiza o rankeamento das ações com base em indicadores financeiros configuráveis, permitindo uma análise eficiente e personalizada.

#### Métodos

- **`__init__(self, df: pd.DataFrame)`**: Construtor da classe, recebe um DataFrame contendo os dados das ações como parâmetro.

- **`_nota(self, resultado_indicador, meta_indicador, tipo_meta, peso) -> float`**: Método privado para calcular a pontuação de um indicador com base em uma meta, tipo de meta e peso especificados.

- **`_pontos(self, df: pd.DataFrame) -> float`**: Método privado para calcular a pontuação total de uma ação, somando as pontuações de cada indicador ponderadas.

- **`aprovados(self) -> pd.DataFrame`**: Método principal que calcula a pontuação para cada ação, classifica as ações por pontuação e retorna um DataFrame contendo apenas as ações aprovadas, ou seja, aquelas com pontuação igual ou superior a 80.

## 5 Utilização

### Exemplo Básico

```python
# Importando o módulo
from src.module import Dados, Rankeamento

# Criando uma instância da classe Dados
dados = Dados("caminho/do/seu/arquivo.csv")

# Obtendo a tabela de dados formatada
tabela_formatada = dados.tabela_status_invest()

# Criando uma instância da classe Rankeamento
rankeamento = Rankeamento(tabela_formatada)

# Obtendo as ações aprovadas
acoes_aprovadas = rankeamento.aprovados()

# Exibindo o resultado
print(acoes_aprovadas)
```

Este código exemplo ilustra o processo básico de utilização do módulo, carregando dados, formatando-os e obtendo as ações aprovadas com pontuação maior ou igual a 80.

## 6 Configuração dos Parâmetros

### Parâmetros de Avaliação do Indicador

A classe `Rankeamento` utiliza um dicionário chamado `param_calc_pont` para configurar os parâmetros de avaliação de cada indicador. Cada chave no dicionário representa um indicador financeiro, e os valores associados são uma lista com três elementos: a meta para o indicador, o tipo de meta ('p' para positiva, 'n' para negativa) e o peso do indicador na pontuação final.

Por exemplo:

```python
param_calc_pont = {
    'preco': [50, 'n', 0.05],
    'dy'   : [6 , 'p', 0.1 ],
    # ...
}
```

Aqui, para o indicador 'preco', a meta é 50, é uma meta negativa ('n') e o peso é 0.05 na pontuação final.

Recomenda-se revisar e ajustar esses parâmetros de acordo com os requisitos específicos da análise financeira desejada.

## Observações

- Certifique-se de ter as bibliotecas Pandas e NumPy instaladas antes de utilizar este módulo.

- O esquema de colunas (`schema`) na classe `Dados` deve ser adaptado conforme a estrutura real do arquivo CSV utilizado.

- A classe `Rankeamento` utiliza percentis para determinar as metas de alguns indicadores. Certifique-se de compreender os dados de entrada e ajuste conforme necessário.

- Recomenda-se revisar e adaptar os pesos e as metas dos indicadores na classe `Rankeamento` para atender aos requisitos específicos da análise financeira desejada; o somatório dos pesos sempre deve ser igual a 1 (ou 100%).