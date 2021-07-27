# Capstone Pipeline

The goal of this capstone project is to create a crypto trading bot that can place trades on the Binance marketplace platform. The stages of the project can be broken up into the following parts: obtaining the financial data, creating the pipeline to extract/transform/store the data, creating the framework for which the bot to place trades, and integrating the bots trades to execute within Binance.

## Step 1

1. Websockets (data extraction) - The financial data is extracted from Binance via websockets and the websocket client. For clarification, the module we use is WEBSOCKETS as opposed to WEBSOCKET which has a slightly different functionality. For our purposes, we used WEBSOCKETS which also requires us to download the module asyncio which will allow us to run the messages obtained from the websockets.connect method asynchronously. The websocket string used to connect to binance is socket = f'wss://stream.binance.com:9443/ws/{cc1}t@kline_{interval}/{cc2}t@kline_{interval}/{cc3}t@kline_{interval}'

2. KafkaProducer (data extraction/wrangling) - Using the information from the websockets, we extract the messages via a json format and send the message to the KafkaProducer via the kafka module (from kafka import KafkaProducer) and send the message via the command producer.send('KafkaStreams', json.dumps(message).encode('utf-8')).

   -Local Machines: To run the KafkaProducer on your local machine, ensure that Apache Kafka (ver 2.6) and Zookeeper are installed. You will then need to change your         bootstrap server to your local host machine. For my local machine it is bootstrap_servers = ['localhost:9092']
   
   -AWS MSK: Amazon has a service called AWS MSK which allows for the creation of a virtual machine (Linux or Windows) to be hosted on their EC2 platform which then        connects to MSK. This allows for Amazon to handle instances of zookeeper (which runs in the background) leaving the heavy lifting to their servers.                      This is the approach I chose to 'play with.' This will change the bootstrap_server to the cluster location housed within the EC2 machine and the                          bootstrap TL within. In order to sync with AWS MSK, I chose to SSH into EC2 via Putty and migrated my local Python documents into the EC2 instance                        via WindowsSCP.

3. KafkaConsumer (data loading) - From the KafkaProducer, we obtain the json messages and decode the utf-8 encoding in order to read the messages.

For further information over how to integrate the websocket client, please refer to the source documentation here: https://pypi.org/project/websocket-client/
