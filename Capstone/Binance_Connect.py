from Capstone_Consumer import kafkaconsumer, boto_trading, boto_connect, main, returns_values
from binance import Client
import asyncio, logging

logging.basicConfig(filename = 'Binance_Connect', level = logging.WARNING)

client = Client('suLnXCgP2OViD5DhC58jLRk1Y8eyVZHwkRpVSxuYYOyEytgrFMEsvAna9s5eS41P',
              'sND90kr7b6thNRZRIOYnqcUVcnu9KFL1U9aqsCyUFWbT1QYxxLz2mVTeFZ4fbJCc', tld = 'us')


account_info = client.get_account()
btc_wallet = account_info['balances'][0]['free']
eth_wallet = account_info['balances'][1]['free']
usd_wallet = account_info['balances'][2]['free']
doge_wallet = account_info['balances'][21]['free']

eth_time_tracker = []
btc_time_tracker = []
doge_time_tracker = []
buy_price = 0
sell_price = 0
test_purchase = 0

async def auto_trade(ticker, tracker = 0):
    reader = await kafkaconsumer(some_topic = ticker, trade = True)
    if reader[2] == 'ETHUSDT':
        d={}
        try:
            current = float(reader[4])
            previous = float(eth_time_tracker[len(eth_time_tracker) - 1]['close'])
            # Logic - close seems to be more dynamic as opposed to opening candles. We should trade based on \
            # What has most volatility, so we will match closing candle prices to closing candle prices
            # If prior close is greater than current close and the difference is greater than 1%: Buy
            buy = previous < current and abs((current - previous)/ previous) > 0.0001 #REMEMBER TO MAKE THIS 0.001!
            #print(previous)
            #print(current)
            #print(f'Buy: {buy}')
            # If prior close is greater than current close and the difference is greater than 1%: Buy
            sell = previous < current and abs((current - previous)/ previous) < 0.0001 #REMEMBER TO MAKE THIS 0.001!
            #print(f'Sell: {sell}')

            if buy == True:
                print('within buy')
                # For ETH, min qty must be of precision 8, 0.00001 min qty, min notional of $10 USD, min stepsize 0.00001
                stepsize = 0.00001
                # Call your account information within binance
                account_info = client.get_account()
                usd_wallet = float(account_info['balances'][2]['free'])

                # pct_spend is the amount you can spend based on what you have in your wallet
                pct_spend = .00001*current/usd_wallet
                print(pct_spend, type(pct_spend))

                # qty_pct is the quantity you want. Ensure that this is inline with min qty AND stepsize
                qty_pct = (usd_wallet * pct_spend / current)
                print(qty_pct, type(qty_pct))

                if qty_pct*100000 % stepsize*100000 < 0:
                    purchase = 0.00001000
                if qty_pct * 100000 % stepsize * 100000 > 0:
                    mod = qty_pct * 100000 % stepsize
                    purchase = ((qty_pct * 100000) - mod)/100000

                # Execute your order
                '''
                The code snippet below is for buying/selling crypto within Binance:
                client.create_order(symbol = 'ETHUSDT', side = 'BUY', type = 'MARKET', quantity = purchase)
                usd_wallet = account_info['balances'][2]['free']
                '''
                # This is to calculate what we purchased. Obviously, since this is a market order and there may be some delays
                # thus it may not be equal to what we would actually query if we use a client.get_account from our binance
                # account.
                usd_wallet = usd_wallet - (purchase * current)
                print(usd_wallet, 'usd_wallet')

                boto_trading('ETH_Crypto', reader, usd_wallet, buy = True, sell = False)

                # You should implement something to track your wallet for crypto. This can further be accessed via
                # the code snippet above, however to track it here would deviate from our ultimate end goal of linking
                # to binance
            if sell == True:
                print('within sell')
                stepsize = 0.00001
                # Call your account information within binance. We want our Ether wallet here because we cannot sell what we
                # do not have
                account_info = client.get_account()
                eth_wallet = account_info['balances'][1]['free'] # since our wallet is actually 0, for debugging lets set it to 10
                eth_wallet = 10

                # pct_spend is the amount you can sell based on what you have in your wallet
                pct_spend = .00001 * current / eth_wallet
                print(pct_spend, type(pct_spend))

                # qty_pct is the quantity you want. Ensure that this is inline with min qty AND stepsize
                qty_pct = (eth_wallet * pct_spend / current)
                print(qty_pct, type(qty_pct))

                if qty_pct * 100000 % stepsize * 100000 < 0:
                    sold = 0.00001000
                if qty_pct * 100000 % stepsize * 100000 > 0:
                    mod = qty_pct * 100000 % stepsize
                    sold = ((qty_pct * 100000) - mod) / 100000

                eth_wallet = eth_wallet + (sold * current)
                print(eth_wallet, 'eth_wallet')

                boto_trading('ETH_Crypto', reader, eth_wallet, buy=False, sell= reader[4])

            # Append the most recent records to the eth_time_tracker
            d['time'], d['open'], d['close'], d['high'], d['low'] = reader[1], reader[3], reader[4], reader[5], reader[6]
            eth_time_tracker.append(d)
        except:
            d['time'], d['open'], d['close'], d['high'], d['low'] = reader[1], reader[3], reader[4], reader[5], reader[6]
            eth_time_tracker.append(d)

    return await execute(eth_time_tracker)

    if reader[2] == 'BTCUSDT':
        d2 = {}
        try:
            current = float(reader[4])
            previous = float(btc_time_tracker[len(btc_time_tracker) - 1]['close'])
            buy = previous < current and abs((current - previous) / previous) > 0.0001  # REMEMBER TO MAKE THIS 0.001!
            sell = previous < current and abs((current - previous) / previous) < 0.0001  # REMEMBER TO MAKE THIS 0.001!

            if buy == True:
                print('within buy')
                stepsize = 0.00001
                account_info = client.get_account()
                usd_wallet = float(account_info['balances'][2]['free'])
                pct_spend = .00001 * current / usd_wallet
                print(pct_spend, type(pct_spend))
                qty_pct = (usd_wallet * pct_spend / current)
                print(qty_pct, type(qty_pct))
                if qty_pct * 100000 % stepsize * 100000 < 0:
                    purchase = 0.00001000
                if qty_pct * 100000 % stepsize * 100000 > 0:
                    mod = qty_pct * 100000 % stepsize
                    purchase = ((qty_pct * 100000) - mod) / 100000
                # Execute your order
                '''
                The code snippet below is for buying/selling crypto within Binance:
                client.create_order(symbol = 'ETHUSDT', side = 'BUY', type = 'MARKET', quantity = purchase)
                usd_wallet = account_info['balances'][2]['free']
                '''
                usd_wallet = usd_wallet - (purchase * current)
                print(usd_wallet, 'usd_wallet')

                boto_trading('BTC_Crypto', reader, usd_wallet, buy=True, sell=False)

            if sell == True:
                print('within sell')
                stepsize = 0.00001
                account_info = client.get_account()
                btc_wallet = account_info['balances'][1]['free']  # since our wallet is actually 0, for debugging lets set it to 10
                btc_wallet = 10

                pct_spend = .00001 * current / btc_wallet
                print(pct_spend, type(pct_spend))

                qty_pct = (btc_wallet * pct_spend / current)
                print(qty_pct, type(qty_pct))

                if qty_pct * 100000 % stepsize * 100000 < 0:
                    sold = 0.00001000
                if qty_pct * 100000 % stepsize * 100000 > 0:
                    mod = qty_pct * 100000 % stepsize
                    sold = ((qty_pct * 100000) - mod) / 100000

                btc_wallet = btc_wallet + (sold * current)
                print(btc_wallet, 'btc_wallet')

                boto_trading('BTC_Crypto', reader, btc_wallet, buy=False, sell=reader[4])

            d2['time'], d2['open'], d2['close'], d2['high'], d2['low'] = reader[1], reader[3], reader[4], reader[5], reader[6]
            btc_time_tracker.append(d2)
        except:
            d2['time'], d2['open'], d2['close'], d2['high'], d2['low'] = reader[1], reader[3], reader[4], reader[5], reader[6]
            btc_time_tracker.append(d2)

    return await execute(btc_time_tracker)

    if reader[2] == 'DOGEUSDT':
        d3 = {}
        try:
            current = float(reader[4])
            previous = float(doge_time_tracker[len(doge_time_tracker) - 1]['close'])
            buy = previous < current and abs((current - previous) / previous) > 0.0001  # REMEMBER TO MAKE THIS 0.001!
            sell = previous < current and abs((current - previous) / previous) < 0.0001  # REMEMBER TO MAKE THIS 0.001!

            if buy == True:
                print('within buy')
                stepsize = 0.00001
                account_info = client.get_account()
                usd_wallet = float(account_info['balances'][2]['free'])
                pct_spend = .00001 * current / usd_wallet
                print(pct_spend, type(pct_spend))
                qty_pct = (usd_wallet * pct_spend / current)
                print(qty_pct, type(qty_pct))
                if qty_pct * 100000 % stepsize * 100000 < 0:
                    purchase = 0.00001000
                if qty_pct * 100000 % stepsize * 100000 > 0:
                    mod = qty_pct * 100000 % stepsize
                    purchase = ((qty_pct * 100000) - mod) / 100000
                # Execute your order
                '''
                The code snippet below is for buying/selling crypto within Binance:
                client.create_order(symbol = 'ETHUSDT', side = 'BUY', type = 'MARKET', quantity = purchase)
                usd_wallet = account_info['balances'][2]['free']
                '''
                usd_wallet = usd_wallet - (purchase * current)
                print(usd_wallet, 'usd_wallet')

                boto_trading('DOGE_Crypto', reader, usd_wallet, buy=True, sell=False)

            if sell == True:
                print('within sell')
                stepsize = 0.00001
                account_info = client.get_account()
                doge_wallet = account_info['balances'][1][
                    'free']  # since our wallet is actually 0, for debugging lets set it to 10
                doge_wallet = 10

                pct_spend = .00001 * current / doge_wallet
                print(pct_spend, type(pct_spend))

                qty_pct = (doge_wallet * pct_spend / current)
                print(qty_pct, type(qty_pct))

                if qty_pct * 100000 % stepsize * 100000 < 0:
                    sold = 0.00001000
                if qty_pct * 100000 % stepsize * 100000 > 0:
                    mod = qty_pct * 100000 % stepsize
                    sold = ((qty_pct * 100000) - mod) / 100000

                doge_wallet = doge_wallet + (sold * current)
                print(doge_wallet, 'doge_wallet')

                boto_trading('DOGE_Crypto', reader, doge_wallet, buy=False, sell=reader[4])

            d3['time'], d3['open'], d3['close'], d3['high'], d3['low'] = reader[1], reader[3], reader[4], reader[5], \
                                                                         reader[6]
            doge_time_tracker.append(d3)
        except:
            d3['time'], d3['open'], d3['close'], d3['high'], d3['low'] = reader[1], reader[3], reader[4], reader[5], \
                                                                         reader[6]
            doge_time_tracker.append(d3)

    return await execute(doge_time_tracker)


async def execute(tracker=0):
    await asyncio.gather (
    auto_trade('ETHUSD', tracker),
    auto_trade('BTCUSD', tracker),
    auto_trade('DOGE', tracker)
    )

'''
client.create_order(symbol = symbol, side = 'BUY', type = 'MARKET', quantity = qty)

'''


if __name__== '__main__':
    trade = asyncio.run(execute())