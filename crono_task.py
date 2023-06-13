import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta
import argparse
import click

# Estabelecer a conexão com o banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='horas_atividades'
)

# Criar a tabela de atividades se ela não existir
create_table_query = '''
    CREATE TABLE IF NOT EXISTS atividades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(255),
        data_hora_inicio DATETIME,
        data_hora_fim DATETIME
    )
'''
cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()

# Função para registrar uma nova atividade
def registrar_atividade(descricao):
    data_hora_inicio = datetime.now()
    data_hora_fim = None

    # Inserir a nova atividade no banco de dados
    insert_query = '''
        INSERT INTO atividades (descricao, data_hora_inicio, data_hora_fim)
        VALUES (%s, %s, %s)
    '''
    values = (descricao, data_hora_inicio, data_hora_fim)
    cursor.execute(insert_query, values)
    conn.commit()

    print('Atividade registrada com sucesso!')

# Função para finalizar a atividade atual
def finalizar_atividade():
    atividade_atual = obter_atividade_atual()

    if atividade_atual:
        atividade_id, _, data_hora_inicio, _ = atividade_atual
        data_hora_fim = datetime.now()

        # Atualizar o registro da atividade no banco de dados
        update_query = '''
            UPDATE atividades
            SET data_hora_fim = %s
            WHERE id = %s
        '''
        values = (data_hora_fim, atividade_id)
        cursor.execute(update_query, values)
        conn.commit()

        print('Atividade finalizada com sucesso!')
    else:
        print('Nenhuma atividade em andamento.')

# Função para obter a atividade atual em andamento
def obter_atividade_atual():
    select_query = '''
        SELECT id, descricao, data_hora_inicio, data_hora_fim
        FROM atividades
        WHERE data_hora_fim IS NULL
        ORDER BY id DESC
        LIMIT 1
    '''
    cursor.execute(select_query)
    return cursor.fetchone()

# Função para obter todas as atividades realizadas
def obter_todas_atividades():
    select_query = '''
        SELECT id, descricao, data_hora_inicio, data_hora_fim
        FROM atividades
        ORDER BY id
    '''
    cursor.execute(select_query)
    return cursor.fetchall()

# Função para calcular o tempo gasto em uma atividade
def calcular_tempo_gasto(data_hora_inicio, data_hora_fim):
    if data_hora_fim is None:
        data_hora_fim = datetime.now()

    tempo_gasto = relativedelta(data_hora_fim, data_hora_inicio)
    return tempo_gasto


# Função para formatar o tempo no formato de dias, horas, minutos e segundos
def formatar_tempo(tempo):
    horas = tempo.hours
    minutos = tempo.minutes
    segundos = tempo.seconds

    dias = horas // 24
    horas = horas % 24

    return f'{dias} dias, {horas} horas, {minutos} minutos, {segundos} segundos'

# Função para obter o tempo agrupado gasto em todas as atividades com a mesma descrição
def obter_tempo_agrupado_por_descricao():
    select_query = '''
        SELECT descricao, SUM(TIMESTAMPDIFF(SECOND, data_hora_inicio, data_hora_fim)) AS tempo_agrupado
        FROM atividades
        WHERE data_hora_fim IS NOT NULL
        GROUP BY descricao
        HAVING COUNT(*) > 1
    '''
    cursor.execute(select_query)
    return cursor.fetchall()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('descricao')
def iniciar(descricao):
    registrar_atividade(descricao)

@cli.command()
def finalizar():
    atividade_atual = obter_atividade_atual()

    if atividade_atual:
        finalizar_atividade()
    else:
        print('Nenhuma atividade em andamento.')

@cli.command()
def listar():
    atividades = obter_todas_atividades()

    if atividades:
        for atividade in atividades:
            atividade_id, descricao, data_hora_inicio, data_hora_fim = atividade
            tempo_gasto = calcular_tempo_gasto(data_hora_inicio, data_hora_fim)

            print(f'ID: {atividade_id}')
            print(f'Descrição: {descricao}')
            print(f'Data e Hora de Início: {data_hora_inicio.strftime("%d/%m/%Y %H:%M:%S")}')
            print(f'Data e Hora de Fim: {data_hora_fim.strftime("%d/%m/%Y %H:%M:%S") if data_hora_fim else "Em andamento"}')
            print(f'Tempo Gasto: {formatar_tempo(tempo_gasto)}')
            print('---')
    else:
        print('Nenhuma atividade registrada.')

    tempo_agrupado = obter_tempo_agrupado_por_descricao()
    if tempo_agrupado:
        print('Tempo Agrupado:')
        for descricao, tempo in tempo_agrupado:
            print(f'Descrição: {descricao}')
            print(f'Tempo Agrupado: {formatar_tempo(relativedelta(seconds=tempo))}')
            print('---')

if __name__ == '__main__':
    cli()
