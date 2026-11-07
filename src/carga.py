import sqlite3

class SalvarDf:
    def __init__(self, df, caminho_do_banco):
        self.df = df
        self.caminho_do_banco = caminho_do_banco
    
    def salvar_sqlite(self):
        """Esse método vai salvar o df,
        para enviarmos ele ao SQLite"""
        conexao = sqlite3.connect(self.caminho_do_banco)
        try:
            self.df.to_sql(name='atendimentos',
                con=conexao,
                if_exists='replace',
                index=False)
            print("DataFrame salvo!")
        finally:
            conexao.close()