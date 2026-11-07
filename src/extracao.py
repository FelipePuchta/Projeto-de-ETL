import pandas as pd

class Extracao:
    def __init__(self, caminho):
        self.caminho = caminho
        
    def extrair_csv(self):
        """Essa função vai ser responsável por
        extrair o arquivo CSV que contém as
        informações dos pacientes"""
        df = pd.read_csv(self.caminho)
        return df
        

if __name__ == "__main__":
    arquivo = Extracao("/Users/felipepuchta/Documents/ChatGPT/Projeto Triagem de Pacientes/dados/brutos/atendimentos.csv")
    df = arquivo.extrair_csv()

    print(df.head())
    print(df.shape) 
