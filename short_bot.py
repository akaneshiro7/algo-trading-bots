import config
from trading_bot import TradingBot

short_spy = TradingBot(config.SPY_SYMBOLS, 'sell', live_trading=True)
short_spy.run()