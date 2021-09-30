from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, date, datetime
import os
import yfinance as yf
import pandas as pd

# git clone https://github.com/puckel/docker-airflow.git
# to run via docker, use the command:
# docker-compose -f docker-compose-LocalExecutor.yml up

# use the command below to log INTO your container and download files. use CTRL D to exit
#  docker exec -ti 8ffd483e5f8f /bin/bash

# To intialize stock data for TSLA and APPL and create callable python functions
def tsla():
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    tsla_df = yf.download('TSLA', start = start_date, end = end_date, interval = '1m')
    tsla_df.to_csv('tsla_data.csv', header = False)
    path = os.path.abspath('tsla_data.csv')
    print(path)


def aapl():
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    aapl_df = yf.download('AAPL', start = start_date, end = end_date, interval = '1m')
    aapl_df.to_csv('aapl_data.csv', header = False)
    path = os.path.abspath('appl_data.csv')
    print(path)

def callable_function():
    aapl_df = pd.read_csv('/tmp/data/'+str(date.today())+'/aapl_data.csv', header = 0)
    tsla_df = pd.read_csv('/tmp/data/'+str(date.today())+'/tsla_data.csv', header = 0)
    return aapl_df, tsla_df

default_args = {
    'owner': 'Tickers',
    'start_date': datetime(2021, 9, 30),
    'retries': 2,
    'retry_delay': timedelta(minutes = 5)
}
# To create the initial dag
dag = DAG(
    'marketvol',
    default_args = default_args,
    description = 'A simple DAG',
    schedule_interval = timedelta(days = 1)
)

# To create python operators for both TSLA and AAPL

t0 = BashOperator(
    task_id = 'Init_Bash_Operator',
    bash_command = 'mkdir -p /tmp/data/'+str(date.today()),
    dag = dag
)
t1 = PythonOperator(
    task_id = 'TSLA_Python',
    python_callable=tsla,
    dag = dag
)

t2 = PythonOperator(
    task_id = 'AAPL_Python',
    python_callable=aapl,
    dag = dag
)
t3 = BashOperator(
    task_id = 'TSLA_Bash',
    bash_command = 'mv /usr/local/airflow/tsla_data.csv' ' /tmp/data/' + str(date.today()),
    dag = dag
)

t4 = BashOperator(
    task_id = 'Aapl_Bash',
    bash_command = 'mv /usr/local/airflow/aapl_data.csv' ' /tmp/data/' + str(date.today()),
    dag = dag
)

t5 = PythonOperator(
    task_id = 'Query',
    python_callable = callable_function,
    dag = dag
)

# Job dependencies
t0>>t1>>t2>>t3>>t4>>t5