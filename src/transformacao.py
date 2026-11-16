import pandas as pd

class Transformacao:
    def __init__(self, df):
        self.df = df.copy()
        self.dados_originais = df.copy() # Preserva os valores antes do tratamento.
        self.problemas = pd.DataFrame(
            columns=['id_atendimento', 'campo', 'valor_original', 'problema']
        )
        
    def registrar_problemas(self, mascara, campo, problema):
        """Acrescenta ao relatório os atendimentos que apresentam um problema"""
        registros = self.df.loc[mascara, ['id_atendimento']].copy()
        if registros.empty:
            return

        registros['campo'] = campo
        registros['valor_original'] = self.dados_originais.loc[registros.index, campo].astype('object')
        registros['problema'] = problema
        self.problemas = pd.concat([self.problemas, registros], ignore_index=True)
        # Evita repetir o mesmo problema quando uma validação é chamada novamente.
        self.problemas = self.problemas.drop_duplicates(ignore_index=True)

    def diagnosticar(self):
        """Essa função realiza um diganóstico geral sobre
        o arquivo analisado. Mostrando coisas como: duplicatas, 
        ausências e etc"""
        self.df.info() # Utilizado para mostrar os tipos das colunas
        print(self.df.isna().sum()) 
        print(self.df.duplicated().sum()) 
    
    def remover_duplicatas(self):
        """Essa função irá remover duplicatas"""
        antes = len(self.df) 
        self.df = self.df.drop_duplicates() # Remove as linhas duplicadas e mantém a primeira (original)
        depois = len(self.df)
        resultado = antes - depois
        print(f"Quantidade de linhas antes: {antes}. Quantidade de linhas depois: {depois}.")
        print(f"Duplicatas: {resultado}")
    
    def normalizar_textos(self):
        """Essa função irá normalizar palavras/textos, 
        para melhores análises"""
        colunas = ['especialidade', 'classificacao_risco', 'desfecho']
        for coluna in colunas:
            self.df[coluna] = self.df[coluna].str.strip().str.lower()
    
    def converter_datas(self):
        """Converte as três colunas de datas, aceitando os dois formatos da base."""
        colunas = ['data_hora_chegada', 'data_hora_inicio_atendimento', 'data_hora_saida'] # Aqui eu defini as colunas que serão convertidas
        for coluna in colunas:
            # Usa o texto original também quando a transformação é executada novamente.
            original = self.dados_originais.loc[self.df.index, coluna]
            convertida = pd.to_datetime(
                original,
                format="%Y-%m-%d %H:%M:%S",
                errors="coerce")
            faltantes = convertida.isna()
            convertida.loc[faltantes] = pd.to_datetime(
                original.loc[faltantes],
                format="%d/%m/%Y %H:%M:%S",
                errors="coerce")

            invalidas = original.notna() & convertida.isna()
            self.registrar_problemas(invalidas, coluna, 'data inválida')
            self.registrar_problemas(original.isna(), coluna, 'data ausente')
            self.df[coluna] = convertida

    def validar_idades(self):
        """Trata idades inválidas como ausentes, sem remover atendimentos"""
        idades = pd.to_numeric(self.df['idade'], errors='coerce')

        textos_invalidos = self.df['idade'].notna() & idades.isna()
        fora_do_intervalo = (idades < 0) | (idades > 100)
        fracionarias = (idades % 1 != 0) & idades.notna()

        invalidas = textos_invalidos | fora_do_intervalo | fracionarias
        contagem_de_invalidas = invalidas.sum()
        print(f"Quantidade de idades inválidas: {contagem_de_invalidas}")
        self.registrar_problemas(invalidas, 'idade', 'idade inválida')
        idades.loc[invalidas] = float('nan')
        self.df['idade'] = idades.astype('Int64')
    
    def validar_cronologia(self):
        """Sinaliza datas ausentes ou fora de ordem, sem remover os registros"""
        colunas = ['data_hora_chegada', 'data_hora_inicio_atendimento', 'data_hora_saida']
        datas_presentes = self.df[colunas].notna().all(axis=1)
        inicio_valido = self.df['data_hora_inicio_atendimento'] >= self.df['data_hora_chegada']
        saida_valida = self.df['data_hora_saida'] >= self.df['data_hora_inicio_atendimento']
        self.df['cronologia_valida'] = datas_presentes & inicio_valido & saida_valida
        quantidade_invalidas = (~self.df['cronologia_valida']).sum()
        print(f"Quantidade de cronologias inválidas: {quantidade_invalidas}")

        inicio_anterior = self.df['data_hora_inicio_atendimento'] < self.df['data_hora_chegada']
        saida_anterior = self.df['data_hora_saida'] < self.df['data_hora_inicio_atendimento']
        self.registrar_problemas(inicio_anterior, 'data_hora_inicio_atendimento', 'início antes à chegada')
        self.registrar_problemas(saida_anterior, 'data_hora_saida', 'saída antes do início do atendimento')

    def calcular_tempos(self):
        """Calcula espera e permanência em minutos apenas para cronologias válidas"""
        validas = self.df['cronologia_valida']
        self.df['tempo_espera_min'] = float('nan')
        self.df['tempo_permanencia_min'] = float('nan')
        self.df.loc[validas, 'tempo_espera_min'] = (
            self.df.loc[validas, 'data_hora_inicio_atendimento']
            - self.df.loc[validas, 'data_hora_chegada']
        ).dt.total_seconds() / 60
        self.df.loc[validas, 'tempo_permanencia_min'] = (
            self.df.loc[validas, 'data_hora_saida']
            - self.df.loc[validas, 'data_hora_chegada']
        ).dt.total_seconds() / 60

    def transformar(self):
        """Executa os métodos em ordem e retorna o DataFrame tratado"""
        self.remover_duplicatas()
        self.normalizar_textos()
        self.converter_datas()
        self.validar_idades()
        self.validar_cronologia()
        self.calcular_tempos()
        return self.df
