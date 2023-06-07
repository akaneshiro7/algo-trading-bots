import config
from trading_bot import TradingBot

long_iwm = TradingBot(config.IWM_SYMBOLS, 'buy', live_trading=True)
long_iwm.run()