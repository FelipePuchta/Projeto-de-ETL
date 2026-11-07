# Projeto-de-ETL
Pipeline ETL em Python para extração, limpeza e validação de dados sintéticos de milhares de atendimentos de pacientes, com exportação de um arquivo tratado para análise.

## Status: em desenvolvimento

Primeira versão de um projeto educacional com dados inteiramente sintéticos.
A extração e a transformação estão implementadas. A carga, a integração em
`main.py` e as consultas SQL serão adicionadas nas próximas etapas.

## Implementado

- Leitura de CSV com pandas.
- Diagnóstico de valores ausentes e duplicatas.
- Remoção de duplicatas e padronização de textos.
- Conversão de datas em dois formatos.
- Tratamento de idades fora do domínio definido para o exercício (0 a 100 anos).
- Sinalização de cronologias inválidas.
- Cálculo de espera e permanência para registros com cronologia válida.

## Dados

O CSV bruto contém 10.100 linhas: 10.000 atendimentos fictícios e 100 duplicatas
exatas. Inclui problemas intencionais de qualidade para praticar ETL. O arquivo
em `dados/referencia/` é um gabarito e não deve alimentar o pipeline.
Os padrões foram inventados e não representam a operação de um hospital real.
Este projeto não realiza diagnóstico ou classificação clínica de pacientes.

## Dependências

Requer Python 3 e pandas. Na pasta do projeto:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

O teste direto em `src/extracao.py` ainda utiliza um caminho absoluto do ambiente
de desenvolvimento. Para executá-lo em outro computador, ajuste esse caminho
para o CSV local. A execução completa pelo `main.py` ainda não está disponível.

## Próximas etapas

- Implementar a carga dos dados tratados.
- Integrar as etapas no `main.py` com caminhos relativos ao projeto.
- Elaborar consultas SQL e apresentar os resultados.
