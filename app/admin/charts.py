import pandas as pd
from app import db
import json
import plotly


def stats_chart():
    layout = {'height': 350, 'width': 800, 'margin': {'l': 40, 'r': 10, 'b': 80, 't': 10, 'pad': 4},
              'legend': {'orientation': "h", 'x': 0.3, 'y': 1.0}}

    df = pd.read_sql(b'SELECT id, project_id, user_id, created_date FROM interest',
                     db.engine.raw_connection(),
                     index_col='created_date', parse_dates=True)
    df['count'] = range(1, df.index.size + 1)
    graph_data = dict(data=[
        {'x': df.index, 'y': df['count'] / 10, 'name': 'Notes of interest (tens)', 'mode': 'lines', 'type': 'scatter'}],
                      layout=layout)

    df = pd.read_sql(b'SELECT id, project_id, created_by, created_date FROM team',
                     db.engine.raw_connection(),
                     index_col='created_date', parse_dates=True)
    df['count'] = range(1, df.index.size + 1)
    graph_data['data'].append({'x': df.index, 'y': df['count'], 'name': 'Teams', 'mode': 'lines', 'type': 'scatter'})

    df = pd.read_sql(b'SELECT id, created_date FROM project',
                     db.engine.raw_connection(),
                     index_col='created_date', parse_dates=True)
    df['count'] = range(1, df.index.size + 1)
    graph_data['data'].append({'x': df.index, 'y': df['count'], 'name': 'Projects', 'mode': 'lines', 'type': 'scatter'})

    return graph_data


def projects_chart():
    layout = {'height': 150, 'width': 260, 'margin': {'l': 20, 'r': 30, 'b': 50, 't': 10, 'pad': 4},
              'showlegend': False}

    df = pd.read_sql(b"SELECT s.name as Status, count(*) as status_count FROM project p join status s on p.status_id = s.id where s.name = 'New' group by s.name",
                     db.engine.raw_connection(),
                     index_col='Status')
    graph_data = dict(data=[{'x': df.index, 'y': df['status_count'], 'name': 'New', 'type': 'bar'}], layout=layout)

    df = pd.read_sql(b"SELECT s.name as Status, count(*) as status_count FROM project p join status s on p.status_id = s.id where s.name = 'Relisted' group by s.name",
                     db.engine.raw_connection(),
                     index_col='Status')
    graph_data['data'].append({'x': df.index, 'y': df['status_count'], 'name': 'Relisted', 'type': 'bar'})

    df = pd.read_sql(b"SELECT s.name as Status, count(*) as status_count FROM project p join status s on p.status_id = s.id where s.name = 'Live' group by s.name",
                     db.engine.raw_connection(),
                     index_col='Status')
    graph_data['data'].append({'x': df.index, 'y': df['status_count'], 'name': 'Live', 'type': 'bar'})

    df = pd.read_sql(b"SELECT s.name as Status, count(*) as status_count FROM project p join status s on p.status_id = s.id where s.name = 'Taken' group by s.name",
                     db.engine.raw_connection(),
                     index_col='Status')
    graph_data['data'].append({'x': df.index, 'y': df['status_count'], 'name': 'Taken', 'type': 'bar'})

    df = pd.read_sql(b"SELECT s.name as Status, count(*) as status_count FROM project p join status s on p.status_id = s.id where s.name = 'Complete' group by s.name",
                     db.engine.raw_connection(),
                     index_col='Status')
    graph_data['data'].append({'x': df.index, 'y': df['status_count'], 'name': 'Complete', 'type': 'bar'})

    return graph_data
