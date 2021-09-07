from kafka import KafkaConsumer
from binance import Client
import asyncio, boto3

'''
It is important to note that boto3 is used to access any communications between Python and AWS. Additionally, once you install boto, you need a way to access 
your AWS information. For this instance, it was done by installing the AWS command line interface and following the steps outlined here:
https://aws.amazon.com/cli/ and here as well : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation
'''

# To set up the connection to your binance account. Since we are using Binance US, we need tld to indicate US
client = Client('suLnXCgP2OViD5DhC58jLRk1Y8eyVZHwkRpVSxuYYOyEytgrFMEsvAna9s5eS41P',
              'sND90kr7b6thNRZRIOYnqcUVcnu9KFL1U9aqsCyUFWbT1QYxxLz2mVTeFZ4fbJCc', tld = 'us')

account_info = client.get_account()
time = client.get_exchange_info()['timezone']

async def kafkaconsumer(some_topic, trade = False):
    '''
    We async the kafka consumer function as we need to call this function multiple times. Since we call it multiple times and
    it will be running continuously, we need to await it and send the messages to the databses in batches via the asyncio.gather
    command further below.
    '''

    consumer = KafkaConsumer(some_topic,
                             bootstrap_servers=['b-1.kafkastreams.cx66e3.c4.kafka.us-east-2.amazonaws.com:9092'])
    # for local computer it is 'localhost:9092'
    # for AWS it is 'b-1.kafkastreams.cx66e3.c4.kafka.us-east-2.amazonaws.com:9092'

    for rec in consumer:
        rec_data = rec.value.decode('utf-8')
        rec_msg = rec_data.split(',')

        #first and last_msg is to remove characters
        first_msg = rec_msg[0].split("\"")
        last_msg = rec_msg[7].split("\"")
        print(first_msg[1], rec_msg[1],rec_msg[2],rec_msg[3], rec_msg[4], rec_msg[5], rec_msg[6], last_msg[0])

        # to send to AWS DynamoDB and sleep.
        # We need to sleep otherwise the kafkaconsumer will get stuck on the initial function call
        # The immediate if statement below sends ALL messages to Crypto, a historical repository
        if trade == False:
            boto_connect('Crypto', first_msg, rec_msg, last_msg)
            await asyncio.sleep(.01)

        if trade == True:
            return await returns_values(first_msg, rec_msg, last_msg)


async def returns_values(first_msg, rec_msg, last_msg):
    # date_time[0], date_time[1], candle['s'], open, close, high, low, vol
    return [first_msg[1], rec_msg[1],rec_msg[2],rec_msg[3], rec_msg[4], rec_msg[5], rec_msg[6], last_msg[0]]

def boto_connect(some_database, first_msg, rec_msg, last_msg):
    # set up boto3. This instance connects to the historical database
    Primary_column_name = 'Time'
    Primary_Key = 5
    columns = ['Date', 'Time', 'Ticker', 'Open', 'Close', 'High', 'Low', 'Vol']
    client = boto3.client('dynamodb', region_name='us-east-2')
    DB = boto3.resource('dynamodb',
                        region_name='us-east-2',
                        aws_access_key_id='AKIAS4YILQJT7RUYMCFC',
                        aws_secret_access_key='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',
                        verify=False)
    table = DB.Table(some_database)

    # To export information to DynamoDB
    response = table.put_item(
        Item={
            Primary_column_name: Primary_Key,
            columns[0]: str(first_msg[1]),
            columns[1]: str(rec_msg[1]),
            columns[2]: rec_msg[2],
            columns[3]: str(round(float(rec_msg[3]), 4)),
            columns[4]: str(round(float(rec_msg[4]), 4)),
            columns[5]: str(round(float(rec_msg[5]), 4)),
            columns[6]: str(round(float(rec_msg[6]), 4)),
            columns[7]: str(round(float(last_msg[0]), 4))
        }
    )

def boto_trading(some_database, msg, balance, buy = False, sell = False):
    # set up boto3. This instance connects to the historical database
    Primary_column_name = 'Time'
    Primary_Key = 5
    columns = ['Date', 'Time', 'Ticker', 'Purchase_Price', 'Sell_Price', 'Balance']
    client = boto3.client('dynamodb', region_name='us-east-2')
    DB = boto3.resource('dynamodb',
                        region_name='us-east-2',
                        aws_access_key_id='AKIAS4YILQJT7RUYMCFC',
                        aws_secret_access_key='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',
                        verify=False)
    table = DB.Table(some_database)
    if buy == True and sell == False:
        sale = None
    else:
        sale = sell
    # To export information to DynamoDB
    response = table.put_item(
        Item={
            Primary_column_name: Primary_Key,
            columns[0]: str(msg[0]),
            columns[1]: str(msg[1]),
            columns[2]: str(msg[2]),
            columns[3]: str(round(float(msg[4]), 4)),
            columns[4]: sale,
            columns[5]: str(balance)
        }
    )

async def main():
    # To read messages for different cryptos and write them to the database
    await asyncio.gather(
    kafkaconsumer('BTCUSD', trade = True),
    kafkaconsumer('ETHUSD', trade = True),
    kafkaconsumer('DOGE', trade = True)
    )

if __name__=='__main__':
    asyncio.run(main())






