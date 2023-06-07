import pandas as pd
import datetime
live_trading = False
BASE_URL = "https://api.alpaca.markets" if live_trading else "https://paper-api.alpaca.markets"

ORDER_DOLLAR_SIZE = 5000
MOVING_AVERAGE = 20
TODAY = datetime.date.today()
START_DATE = TODAY - datetime.timedelta(days=MOVING_AVERAGE)

def getTickers(filename):
    return pd.read_csv(f'./stocks/{filename}')['Ticker'].tolist()

QQQ_SYMBOLS = getTickers('qqq.csv')
SPY_SYMBOLS = getTickers('spy.csv')
IWM_SYMBOLS = getTickers('iwm.csv')