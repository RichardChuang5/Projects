import websockets
import json
import asyncio
import datetime
from kafka import KafkaProducer


#this is the way we extract information. on message is the type of information we need to extract and on close is what things need to be executed when the link is closed.
#This information is also taken directly from https://pypi.org/project/websocket-client/

cc1 = 'btcusd'
cc2 = 'ethusd'
cc3 = 'dogeusd'
interval = '1m'
socket = f'wss://stream.binance.com:9443/ws/{cc1}t@kline_{interval}/{cc2}t@kline_{interval}/{cc3}t@kline_{interval}'

# To point to the producer that currently sits within our local computer
producer = KafkaProducer(bootstrap_servers=['b-1.kafkastreams.cx66e3.c4.kafka.us-east-2.amazonaws.com:9092'])

async def on_message():
    async with websockets.connect(socket) as crypto_stream:
        while True:
            json_message = json.loads(await crypto_stream.recv())
            candle = json_message['k']
            x=str(datetime.datetime.now())
            date_time=x.split(' ')
            open, close, high, low, vol = candle['o'], candle['c'], candle['h'], candle['l'], candle['v']
            message = ('{},{},{},{},{},{},{},{}'.format(date_time[0], date_time[1], candle['s'], open, close, high, low, vol))
            print(message)
            producer.send('KafkaStreams', json.dumps(message).encode('utf-8'))

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_message())



