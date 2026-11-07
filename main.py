from pathlib import Path
from src.extracao import Extracao
from src.transformacao import Transformacao
from src.carga import SalvarDf


def main():
    """Executa a extração, a transformação e o salvamento dos dados no SQLite"""
    raiz = Path(__file__).resolve().parent
    caminho_csv = raiz / 'dados' / 'brutos' / 'atendimentos.csv'
    caminho_do_banco = raiz / 'banco' / 'atendimentos.db'
    caminho_do_banco.parent.mkdir(parents=True, exist_ok=True)

    print("Iniciando a extração dos dados...")
    arquivo = Extracao(caminho_csv)
    df = arquivo.extrair_csv()

    print("Iniciando a transformação dos dados...")
    transformacao = Transformacao(df)
    df_tratado = transformacao.transformar()

    print("Salvando os dados no SQLite...")
    carga = SalvarDf(df_tratado, caminho_do_banco)
    carga.salvar_sqlite()

    print(f"ETL concluído! Quantidade de atendimentos: {len(df_tratado)}")
    print(f"Banco salvo em: {caminho_do_banco}")


if __name__ == "__main__":
    main()
