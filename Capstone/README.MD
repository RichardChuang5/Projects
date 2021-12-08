# Capstone Pipeline Project - Cryptocurrency Trading

![image](https://user-images.githubusercontent.com/80606434/134072126-37f2de08-bd5d-4be2-854a-e0059854eef5.png)

The goal of this project is to create a crypto trading bot that can place trades on the Binance marketplace platform and store the details of the trade on a cloud based storage platform. The stages of the project can be broken up into the following parts: obtaining the financial data, creating the pipeline to extract/transform/store the data, creating the framework for which the bot to place trades, and integrating the bots trades to execute within Binance with our focused cryptocurrencies being Bitcoin, Dogecoin, and Ethereum. Overall monitoring of the project will be performed by AWS Cloudwatch.

The general overview of the Python scripts used are as follows
1. **Capstone_Producer -** Responsible for connecting to Binance US via websockets and sending messages via AWS MSK (aka Kafka Streams)
2. **Capstone_Consumer -** Decodes and consumes the messages. Used to send messages to historical transaction tables and record trades taken via boto3
3. **Binance_Connect -** Responsible for providing our trading strategy as well as connecting to our Binance US wallet to create trades and drawdown current wallet information.

## Step 1 - Extraction
![image](https://user-images.githubusercontent.com/80606434/134079538-1d3917c8-c0d7-4698-9d34-71d8c7be8498.png)

1. **Websockets (data extraction) -** The financial data is extracted from Binance via websockets and the websocket client. For clarification, the module we use is WEBSOCKETS as opposed to WEBSOCKET which has a slightly different functionality. For our purposes, we used WEBSOCKETS which also requires us to download the module asyncio which will allow us to run the messages obtained from the websockets.connect method asynchronously. The websocket string used to connect to binance is socket = f'wss://stream.binance.com:9443/ws/{cc1}t@kline_{interval}/{cc2}t@kline_{interval}/{cc3}t@kline_{interval}'

For further information over how to integrate the websocket client, please refer to the source documentation here: https://pypi.org/project/websocket-client/

Messages received come in the form of JSON messages and are decoded to extract ticker, volume, high, low, open, and close price.

## Step 2 - Transformation
![image](https://user-images.githubusercontent.com/80606434/134079630-eba06c85-e0aa-49ff-b943-b59b9ad852a5.png)


1. **Messages received from the websockets are handled through the boto_trading function -** The Python script applies a simple trading methodology known as scalping which buys crypto if the current price has dropped 1% in relation to the prior message price, and sells if it has increased 1%. This is integrated with our Binance US wallet and buys/sells based on a percentage of our overall wallet portfolio. 
   - *It is important to note that for Binance integrations, there are certain formats you must adhere to, otherwise trading is not allowed. For instance, to trade    Ethereum, you must have a stepsize of at least 0.00001, a precision of 8, a minimum quantity of 0.00001, and a minimum notional value of $10 USD. If any of these requirements are not met an error will occur.*

2. **KafkaProducer (data extraction/wrangling) -** Using the information from the websockets, we extract the messages via a json format and send the message to the KafkaProducer via the kafka module (from kafka import KafkaProducer) and send the message via the command producer.send('KafkaStreams', json.dumps(message).encode('utf-8')).
   - **Local Machines:** To run the KafkaProducer on your local machine, ensure that Apache Kafka (ver 2.6) and Zookeeper are installed. You will then need to change your  bootstrap server to your local host machine. For my local machine it is bootstrap_servers = ['localhost:9092']
   - **AWS MSK:** Amazon has a service called AWS MSK which allows for the creation of a virtual machine (Linux or Windows) to be hosted on their EC2 platform which then connects to MSK and mirrors Apache Kafka hosted on a local machine. This allows for Amazon to handle instances of zookeeper (which runs in the background) leaving the heavy lifting to their servers. This is the approach I chose to 'play with.' This will change the bootstrap_server to the cluster location housed within the EC2 machine and the bootstrap TL within. In order to sync with AWS MSK, I chose to SSH into EC2 via Putty and migrated my local Python documents into the EC2 instance via WindowsSCP.

3. **KafkaConsumer (data loading) -** From the KafkaProducer, we obtain the json messages and decode the utf-8 encoding in order to read the messages.

## Step 3 - Trading & Storage
![image](https://user-images.githubusercontent.com/80606434/134079659-241b2a2f-3a15-49e2-a57b-7af94bffd2f1.png)

1. **Boto3 --> DynamoDB -** Using the KafkaConsumer messages received, we then use Boto3 to sync with our AWS DynamoDB database and send the formatted messages to our database. These messages are sent to our 'Crypto_Table' and serve as an overall repository for historical information.

2. **Binance US Trading -** Using the messages consumed, we will also simultaneously place trades that read the current closing price against the prior closing price for Ethereum, Doge, or Bitcoin. If the price has dropped 1%, then our trading bot will place an order to buy and if the price increases by 1%, assuming we have previously purchased the selected crypto, then the bot will sell it. The details of the trade will be sent to DynamoDB for storage (close, sale price, volume, ticker)

