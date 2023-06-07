import datetime
import pandas as pd
import config
import keys
import sys
from alpaca_trade_api.rest import REST, TimeFrameUnit

class TradingBot:
    def __init__(self, symbols, order_type, live_trading=False):
        pd.set_option('display.max_rows', None)

        self.BASE_URL = "https://api.alpaca.markets" if live_trading else "https://paper-api.alpaca.markets"
        self.API_KEY = keys.API_KEY
        self.SECRET_KEY = keys.SECRET_KEY
        self.symbols = symbols
        self.api = REST(key_id=self.API_KEY, secret_key=self.SECRET_KEY, base_url=self.BASE_URL)
        self.order_type = order_type
    def get_bars(self):
        try:    
            bars = self.api.get_bars(config.symbols, TimeFrame.Day, config.START_DATE, config.TODAY).df
        except Exception as e:
            sys.exit(e)

        bars['previous_close'] = bars['close'].shift(1)
        bars['ma'] = bars['previous_close'].rolling(config.MOVING_AVERAGE).mean()

        return bars

    def filter_bars(self, bars):
        filtered = bars[bars.index.strftime('%Y-%m-%d') == config.TODAY.isoformat()].copy()
        filtered['percent'] = filtered['open'] / filtered['previous_close']

        return filtered

    def find_downgaps(self, filtered):
        downgaps = filtered[filtered['percent'] < 0.98]
        downgaps_below_ma = downgaps[downgaps['open'] < downgaps['ma']]

        return downgaps_below_ma['symbol'].tolist()

    def execute_orders(self, order_symbols, downgaps_below_ma):
        for symbol in order_symbols:
            order_price = downgaps_below_ma[downgaps_below_ma['symbol'] == symbol]['open'].iloc[-1]
            quantity = config.ORDER_DOLLAR_SIZE // order_price

            print('{} shorting {} {} at {}'.format(datetime.datetime.now().isoformat, quantity, symbol, order_price))

            try:
                order = self.api.submit_order(symbol, quantity, self.order_type, 'market')
                print("Order Submitted Successfully: {}".format(order.id))
            except Exception as e:
                print("Error executing the above order {}".format(e))

    def run(self):
        if not self.api.get_clock().is_open:
            sys.exit("Market Closed")

        bars = self.get_bars()
        filtered = self.filter_bars(bars)
        order_symbols = self.find_downgaps(filtered)
        self.execute_orders(order_symbols, filtered)
