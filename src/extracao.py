import pandas as pd

class Extracao:
    def __init__(self, caminho):
        self.caminho = caminho
        
    def extrair_csv(self):
        """Essa função vai ser responsável por
        extrair o arquivo CSV que contém as
        informações dos pacientes"""
        df = pd.read_csv(self.caminho)
        self.validar_colunas(df)
        return df
    
    def validar_colunas(self, df):
        """Esse método vai receber o df e verificar
        se ele possui todas as colunas que ele
        deve possuir"""
        colunas_obrigatorias = [
            'id_atendimento',
            'id_paciente',
            'idade',
            'data_hora_chegada',
            'data_hora_inicio_atendimento',
            'data_hora_saida',
            'classificacao_risco',
            'especialidade',
            'desfecho']
        colunas_faltando = [] # Lista que vai receber as colunas que estão faltando
        for coluna in colunas_obrigatorias:
            if coluna not in df.columns:
                colunas_faltando.append(coluna)
        if colunas_faltando:
            raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(colunas_faltando)}")
        
        

if __name__ == "__main__":
    arquivo = Extracao("/Users/felipepuchta/Documents/ChatGPT/Projeto Triagem de Pacientes/dados/brutos/atendimentos.csv")
    df = arquivo.extrair_csv()

    print(df.head())
    print(df.shape) 
