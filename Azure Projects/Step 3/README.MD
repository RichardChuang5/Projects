# Create cleaned Trade and Quote data

## Purpose
Create Spark DataFrames using Parquet files, performing data cleaning using Spark aggregation methods, and using cloud storage as the output of Spark Jobs.

## Steps
1. Within this project, we extracted data from Parquet files we stored as part of step 2 of the mini project. From there, we reloaded the files from our Azure storage back into our Jupyter notebook in our HD cluster.

2. We then aggregated the information by 'arrival_tm' using the following function

   def applyLatest(item):
    recent_trade = item.groupBy('trade_dt','Symbol','trade_pr/exch', 'event_tm', 'event_seq_nb').agg(functions.max('arrival_tm').alias('max_arrival_time'))
    return recent_trade

3. We then saved the dataframe as an updated Parquet file for both trade and quote data. Saved items can be viewed from the snapshot below

![image](https://user-images.githubusercontent.com/80606434/131577750-c3699137-8477-4fca-a848-7b16d1195fdd.png)
![image](https://user-images.githubusercontent.com/80606434/131578208-0196dbd7-edf4-4c88-a7a6-a0553a8760ab.png)
![image](https://user-images.githubusercontent.com/80606434/131578239-37e8d853-8ffc-4c11-9106-5501cc94d25e.png)

