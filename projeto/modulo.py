import pandas as pd
import numpy  as np

class Dados:
    def __init__(self, arquivo):
        """
        Classe para representar dados de um arquivo CSV.

        Parameters:
            arquivo (str): Caminho do arquivo CSV.
        """
        self.arquivo = arquivo

        self.schema = {
            'TICKER'                 : 'ticker',
            'PRECO'                  : 'preco',
            'DY'                     : 'dy',
            "MARGEM EBIT"            : 'margem_ebit',
            "MARG. LIQUIDA"          : 'margem_liquida',
            'ROE'                    : 'roe',
            "CAGR RECEITAS 5 ANOS"   : 'cagr_rec_5a',
            "CAGR LUCROS 5 ANOS"     : 'cagr_luc_5a',
            " LIQUIDEZ MEDIA DIARIA" : 'liquidez',
            " PEG Ratio"             : 'peg_Ratio'
        }

    def tabela_status_invest(self):
        """
        Lê o arquivo CSV e retorna uma tabela formatada.
        """
        dados = pd.read_csv(self.arquivo, sep=';', usecols=self.schema.keys())
        dados.rename(columns=self.schema, inplace=True)
        dados.dropna(axis='index', how='any', inplace=True)

        return dados


class Rankeamento:
    def __init__(self, df):
        """
        Classe para realizar o rankeamento de ações com base em indicadores.

        Parameters:
            df (pd.DataFrame): DataFrame contendo os dados das ações.
        """
        self.df = df

        # Parâmetros de avaliação do indicador
        self.param_calc_pont = {
            'preco'          : [ 50                                      , 'n' , 0.05      ],
            'dy'             : [ 6                                       , 'p' , 0.1       ],
            'margem_ebit'    : [ np.percentile( self.df['margem_ebit'   ], 85 ), 'p', 0.1  ],
            'margem_liquida' : [ np.percentile( self.df['margem_liquida'], 85 ), 'p', 0.1  ],
            'roe'            : [ np.percentile( self.df['roe'           ], 85 ), 'p', 0.15 ],
            'cagr_rec_5a'    : [ np.percentile( self.df['cagr_rec_5a'   ], 85 ), 'p', 0.2  ],
            'cagr_luc_5a'    : [ np.percentile( self.df['cagr_luc_5a'   ], 85 ), 'p', 0.2  ],
            'liquidez'       : [ np.percentile( self.df['liquidez'      ], 85 ), 'p', 0.05 ],
            'peg_Ratio'      : [ 1                                       , 'n' , 0.05      ]
        }

    def _nota(self, resultado_indicador, meta_indicador, tipo_meta, peso):
        """
        Calcula a pontuação de 1 indicador.

        Parameters:
            resultado_indicador (float): Valor do indicador.
            meta_indicador      (float): Meta do indicador.
            tipo_meta           (str  ): Tipo de meta ('p' para positiva, 'n' para negativa).
            peso                (float): Peso do indicador.

        Returns:
            float: Pontuação do indicador.
        """
        # Verifica se a meta é negativa ou positiva
        if tipo_meta == 'p':
            n = resultado_indicador / meta_indicador * 100 * peso
        else:
            n = (1 - (resultado_indicador - meta_indicador) / meta_indicador) * 100 * peso

        # Nota máxima estabelecida para o indicador
        n_max = (peso * 100)

        # Nota deve estar entre 0 e o Máximo estabelecido
        n = max(0, min(n, n_max))

        return n

    def _pontos(self, df):
        """
        Calcula a pontuação total de uma ação.

        Parameters:
            df (pd.DataFrame): DataFrame contendo os dados de uma ação.

        Returns:
            float: Pontuação total da ação.
        """
        pontuacao = 0

        # Na linha corrente, soma cumulativamente as pontuações de cada coluna/indicador
        for coluna, parametro in self.param_calc_pont.items():
            r = df[coluna]   # Resultado do indicador
            m = parametro[0] # Meta
            t = parametro[1] # Tipo de meta (Negativa ou Positiva)
            p = parametro[2] # Peso do indicador

            pontuacao += self._nota(r, m, t, p)

        return pontuacao

    def aprovados(self):
        """
        Retorna as ações aprovadas com pontuação maior ou igual a 80.

        Returns:
            pd.DataFrame: DataFrame contendo as ações aprovadas.
        """
        df_copy = self.df.copy()  # Dados
        df_copy['pontuacao'] = df_copy.apply(self._pontos, axis=1)  # Calcula pontuação de cada indicador da linha
        df_copy.sort_values('pontuacao', ascending=False, inplace=True)  # Classifica pontuação

        return df_copy.query('pontuacao >= 80').reset_index(drop=True)  # Apenas ações com pontuação >= 80