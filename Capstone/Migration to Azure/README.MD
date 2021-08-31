# PySpark Data Migration

This file serves as documentation to download data from our Amazon AWS DynamoDB database using PySpark and storing the csv files created in Microsoft Azure storage blobs.
The code is run in Jupyter Notebook. 

Step 1: I had to use Amazon's boto3 client to gain access to the database using boto3.client and boto3.resource.
Step 2: Once the client and resources were defined, I just had to query which tables we were accessing (ETH, BTC, or DOGE) and format the data into dataframes.
Step 3: Wrote the dataframes to a csv file using df.write.format and specifying our Azure blob storage.
Step 4: Read from the csv in blob storage to ensure that the file transfer was a success.
