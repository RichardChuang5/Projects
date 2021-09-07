import websockets, json, asyncio, datetime
from kafka import KafkaProducer

#This information is also taken directly from https://pypi.org/project/websocket-client/
cc1 = 'btcusd'
cc2 = 'ethusd'
cc3 = 'dogeusd'
interval = '1m'
socket = f'wss://stream.binance.com:9443/ws/{cc1}t@kline_{interval}/{cc2}t@kline_{interval}/{cc3}t@kline_{interval}'
# To point to the producer that currently sits within our local computer/EC2
producer = KafkaProducer(bootstrap_servers=['xxx'])

async def on_message():
    async with websockets.connect(socket) as crypto_stream:
        while True:
            # To produce msg in JSON format
            json_message = json.loads(await crypto_stream.recv())
            # To only provide kline information
            candle = json_message['k']
            # To create date/time for primary and sorting key used in DynamoDB storing in later steps
            x=str(datetime.datetime.now())
            date_time=x.split(' ')
            # Format data for producing
            open, close, high, low, vol = candle['o'], candle['c'], candle['h'], candle['l'], candle['v']
            message = ('{},{},{},{},{},{},{},{}'.format(date_time[0], date_time[1], candle['s'], open, close, high, low, vol))
            print(message)

            # Current topics online to select from are 'KafkaStreams', 'BTCUSD', 'ETHUSD', and 'DOGE'
            if candle['s'] == 'ETHUSDT':
                producer.send('ETHUSD', json.dumps(message).encode('utf-8'))
            if candle['s'] == 'BTCUSDT':
                producer.send('BTCUSD', json.dumps(message).encode('utf-8'))
            if candle['s'] == 'DOGEUSDT':
                producer.send('DOGE', json.dumps(message).encode('utf-8'))


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    # Current topics online to select from are KafkaStreams, BTCUSD, ETHUSD, and DOGE
    loop.run_until_complete(on_message())



