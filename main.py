from google.cloud import bigquery
# import pandas as pd
import os
import sys
# Importando o arquivo de consultas queries.py
import queries
from queries import PROJECT, DATASET, TABLE
# import itertools
import datetime
from utils import turn_off_system


sys.path.append('..')
# base directory
BASE_DIR = os.path.join(os.path.dirname(__file__))

# adding credentials in enviroment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    BASE_DIR, 'credentials/serasa_google.json')
client = bigquery.Client()


def truncate_table(query):
    '''
        Recebe uma string composta de multilinhas contendo os comandos
        SQL para limpar a tabela
        executa: TRUNCATE TABLE nome_tabela
    '''
    query_job = client.query(query=query)
    result = query_job.result()
    print(f'Limpando dados antigos da tabela {query_job.destination}')
    print(list(result))


def conta_linhas_tbl():
    '''
        faz o controle do total de linhas inserido a cada insercao
    '''
    query_job = client.query(queries.linhas_iniciais_tabela)
    total = query_job.result()

    return total

def atualiza_status_rac_pf(query):
    '''
        Essa funcao recebe como parametro uma string composta de multiplas linhas
        e cria um objeto row do bigquery ao retornar o resultado da funcao
        esse objeto sera usado para executar o insert

    '''
    linhas_i = [row[0] for row in conta_linhas_tbl()]
    query_job = client.query(query)

    result = query_job.result()
    linhas_f = [row[0] for row in conta_linhas_tbl()]

    linhas_inseridas = linhas_f[0] - linhas_i[0]
    print(f'Total de linhas inseridas: {linhas_inseridas}')
    return linhas_inseridas, result


def executa_insert(rows):
    '''
        Recebe um objeto do bigquery Row e percorre o mesmo executando o 
        insert das linhas na tabela definida no inicio do codigo nas
        variaveis PROJETO DATASET e TABLE
    '''
    rows_insert = []
    # for row in itertools.islice(rows, 3):
    for row in rows:
        # obtem os nomes das colunas
        list_k = list(row.keys())

        # constroi o dicionario de valores a serem inseridos
        dick_values = {}
        for i in range(len(list_k)):
            # print(f'Chave: {list_k[i]} e Valor: {row[i]}')
            # valida se a data esta no formato de tupla se tiver converte
            # ela para texto
            if isinstance(row[i], datetime.date):
                dick_values[list_k[i]] = str(row[i])
            else:
                dick_values[list_k[i]] = row[i]

        rows_insert.append(dick_values.copy())

    print(f'Executando o insert de {len(rows_insert)} linhas...')
    client.insert_rows_json(client.get_table(
        f'{PROJECT}.{DATASET}.{TABLE}'), rows_insert)


if __name__ == '__main__':
    # inicio do processo
    start = datetime.datetime.now()

    qs = ['query_1', 'query_2']

    # loop para executar as consultas em sequencia
    for q in qs:
        print(f'Executando a consulta "{q}"')
        # obtem o atributo com o nome da query dentro da lib
        # queries.py -> getattr(queries, nome_da_query)
        query = getattr(queries, q)
        total, rows = atualiza_status_rac_pf(query=query)
        
    print(
        f'Processo finalizado. Tempo total decorrido {datetime.datetime.now() - start}')
    
    print('Desligando VM...')
    turn_off_system()
    