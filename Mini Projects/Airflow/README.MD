# Airflow

The purpose of this mini project is to create a data pipeline to extract online stock market data and deliver analytical results. The Yahoo Finance API is the main data source (yfinance).Yahoo Finance provides intra-day market price details down a one-minute interval.

We will work with two stock symbols: AAPL and TSLA. The workflow should be scheduled to run at 6 PM on every weekday (Mon - Fri), which functions as below:

- Download the daily price data with one minute interval for the two symbols. Each symbol will have a separate task, Task1 (t1) and Task2 (t2), which run independently and in parallel.
- Save both datasets into CSV files and load them into HDFS. Each symbol will have a separate task, Task3 (t3) and Task4 (t4), which run independently and in parallel.
- Run your custom query on the downloaded dataset for both symbols, Task5 (t5). Before this step executes, all previous tasks must complete.
- Use the local executor in Airflow to run the job.

Note: The Airflow environment is set up using Docker based off the image made from Puckel. More information can be found here:
https://github.com/puckel/docker-airflow

With this mini-project, you will utilize Apache Airflow to orchestrate your pipeline, exercise the DAG creation, uses of various operators (BashOperator, PythonOperator, etc), setting up order of operation of each task.
In this mini-project, you will gain familiarity with how to use Apache Airflow to automate data pipelining tasks. Along the way, you will learn how to:
● Use Apache Airflow to orchestrate your pipeline
● Exercise DAG creation
● Use Various Airflow operators like BashOperator and PythonOperator
● Set up the order operation of each task
● Use Celery Executor to run your job

