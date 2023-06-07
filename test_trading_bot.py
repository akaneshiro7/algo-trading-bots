import datetime
import pandas as pd
import pytest
from alpaca_trade_api.rest import REST, TimeFrameUnit
from unittest.mock import MagicMock
from trading_bot import TradingBot

@pytest.fixture
def trading_bot():
    symbols = ['AAPL', 'GOOGL', 'TSLA']
    order_type = 'limit'
    return TradingBot(symbols, order_type)

@pytest.fixture
def mock_api():
    return MagicMock(REST)

@pytest.fixture
def mock_clock():
    return MagicMock()

def test_get_bars(trading_bot, mock_api):
    expected_bars = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA'],
        'open': [100, 200, 300],
        'close': [110, 220, 330],
        'previous_close': [None, 100, 200],
        'ma': [None, None, None]
    })
    mock_api_instance = mock_api.return_value
    mock_api_instance.get_bars.return_value.df = expected_bars

    bars = trading_bot.get_bars()

    assert isinstance(bars, pd.DataFrame)
    assert bars.equals(expected_bars)

def test_filter_bars(trading_bot):
    bars = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA'],
        'open': [100, 200, 300],
        'close': [110, 220, 330],
        'previous_close': [None, 100, 200],
        'ma': [None, None, None]
    })

    filtered = trading_bot.filter_bars(bars)

    assert isinstance(filtered, pd.DataFrame)
    assert filtered.shape == (1, 6)

def test_find_downgaps(trading_bot):
    filtered = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA'],
        'open': [100, 200, 300],
        'close': [110, 220, 330],
        'previous_close': [None, 100, 200],
        'ma': [None, None, None],
        'percent': [0.909, 1.0, 1.5]
    })

    downgaps = trading_bot.find_downgaps(filtered)

    assert isinstance(downgaps, list)
    assert downgaps == ['AAPL']

def test_execute_orders(trading_bot, mock_api):
    order_symbols = ['AAPL']
    downgaps_below_ma = pd.DataFrame({
        'symbol': ['AAPL'],
        'open': [100],
        'close': [110],
        'previous_close': [None],
        'ma': [None],
        'percent': [0.909]
    })

    mock_api_instance = mock_api.return_value
    mock_api_instance.submit_order.return_value.id = '12345'

    trading_bot.execute_orders(order_symbols, downgaps_below_ma)

    mock_api_instance.submit_order.assert_called_once_with('AAPL', 1, 'limit', 'market')
    assert mock_api_instance.submit_order.return_value.id == '12345'

def test_run_market_closed(trading_bot, mock_clock):
    mock_clock_instance = mock_clock.return_value
    mock_clock_instance.is_open = False
    trading_bot.api.get_clock.return_value = mock_clock_instance
    with pytest.raises(SystemExit) as excinfo:
        trading_bot.run()

    assert str(excinfo.value) == 'Market Closed'

def test_run(trading_bot, mock_clock, mock_api):
    mock_clock_instance = mock_clock.return_value
    mock_clock_instance.is_open = True
    trading_bot.api.get_clock.return_value = mock_clock_instance

    expected_bars = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA'],
        'open': [100, 200, 300],
        'close': [110, 220, 330],
        'previous_close': [None, 100, 200],
        'ma': [None, None, None]
    })
    trading_bot.get_bars = MagicMock(return_value=expected_bars)

    filtered = pd.DataFrame({
        'symbol': ['AAPL'],
        'open': [100],
        'close': [110],
        'previous_close': [None],
        'ma': [None],
        'percent': [0.909]
    })
    trading_bot.filter_bars = MagicMock(return_value=filtered)

    order_symbols = ['AAPL']
    trading_bot.find_downgaps = MagicMock(return_value=order_symbols)

    downgaps_below_ma = pd.DataFrame({
        'symbol': ['AAPL'],
        'open': [100],
        'close': [110],
        'previous_close': [None],
        'ma': [None],
        'percent': [0.909]
    })
    trading_bot.execute_orders = MagicMock()

    trading_bot.run()

    trading_bot.get_bars.assert_called_once()
    trading_bot.filter_bars.assert_called_once_with(expected_bars)
    trading_bot.find_downgaps.assert_called_once_with(filtered)
    trading_bot.execute_orders.assert_called_once_with(order_symbols, filtered)
