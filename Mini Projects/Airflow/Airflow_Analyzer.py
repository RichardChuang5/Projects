from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, date, datetime
from pathlib import Path
import os
import yfinance as yf
import pandas as pd

# git clone https://github.com/puckel/docker-airflow.git
# to run via docker, use the command w/in your airflow directory:
# docker-compose -f docker-compose-LocalExecutor.yml up
# don't forget to add airflow scheduler

# use the command below to log INTO your container and download files. use CTRL D to exit
#  docker exec -ti 8ffd483e5f8f /bin/bash

# As our Airflow is run from Docker, we need to modify the docker-compose-localexecutor.yaml file
# to include - ./logs:/usr/local/airflow/logs under our volume profile.
logger = '/Users/yasmeenfuentes/PycharmProjects/pythonProject/Mini-Projects/Airflow/Airflow_Test2/docker-airflow/logs/marketvol'

def analyze_file(**kwargs):
    file_list = Path(logger).rglob('*.log')
    log_path = kwargs['log_path']
    symbol = kwargs['stock_ticker']
    print(file_list)
    list = []
    error_list=[]
    for i in file_list:
        list.append(str(i))
        print(i)
        # To edit th log file
        log_file = open(str(i),'r')
        for line in log_file:
            if 'ERROR' in line:
                error_list.append(line)
                print(error_list)
    task_instance = kwargs['task_instance']
    task_instance.xcom_push(key = 'error_count', value = len(error_list))
    task_instance.xcom_push(key = 'errors', value = error_list)

default_args = {
    'owner': 'Tickers',
    'start_date': datetime(2021, 10, 1)
}

tsla_command = """
    echo -e "total error count:" {{ task_instance.xcom_pull(task_ids='TSLA_logging_errors', key='error_count') }} "\n
    List of errors for TESLA:" {{ task_instance.xcom_pull(task_ids='TSLA_logging_errors', key='errors') }} 
"""
aapl_command = """
    echo -e "total error count:" {{ task_instance.xcom_pull(task_ids='AAPL_logging_errors', key='error_count') }} "\n
    List of errors for AAPL:" {{ task_instance.xcom_pull(task_ids='AAPL_logging_errors', key='errors') }} 
"""
# To create the initial dag
dag = DAG(
    'log_analyzer',
    default_args = default_args,
    description = 'DAG Analysis',
    schedule_interval = "* * * * *"
)

# To create python operators for both TSLA and AAPL

t1 = PythonOperator(
    task_id = 'TSLA_logging_errors',
    python_callable=analyze_file,
    provide_context = True,
    op_kwargs = {'stock_ticker':'TSLA', 'log_path': logger},
    dag = dag
)
t2 = BashOperator(task_id = 'print_TSLA_errors',
                  bash_command = tsla_command,
                  dag = dag)

t3 = PythonOperator(
    task_id = 'AAPL_logging_errors',
    python_callable=analyze_file,
    provide_context = True,
    op_kwargs = {'stock_ticker':'AAPL', 'log_path': logger},
    dag = dag
)
t4 = BashOperator(task_id = 'print_AAPL_errors',
                  bash_command = aapl_command,
                  dag = dag)



# Job dependencies
t1>>t2>>t3>>t4