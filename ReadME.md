# Algo Trading Bot - Down Gap Strategy

This project is about an algorithmic trading bot implemented using Python, pandas, and Alpaca API. The bot executes a specific trading strategy based on the behavior of stocks that gap down at the open. The strategy is described in detail in the article [Should You Buy or Sell Stocks that Gap Down?](https://www.quantrocket.com/blog/buy-or-sell-down-gaps/) on QuantRocket's blog.

## Strategy Summary

The strategy focuses on the concept of stocks gapping down at the open. Traditionally, a common strategy is to buy the gap, expecting mean reversion. However, the implementation in this bot finds a profitable strategy based on selling, not buying, the gap. The reasoning behind the traditional strategy is that bad news causes traders to enter sell orders overnight which execute in tandem at the open, causing a temporary liquidity shock which drives down the opening price. The selling pressure is thought to exhaust itself immediately, leading the stock to recover throughout the remainder of the session. This strategy typically targets stocks in an uptrend, expecting that traders will buy the dip.

The bot first screens a universe of about 2500 listed stocks using the following criteria:

1. Common stocks only (no ETFs, ADRs, or preferred shares)
2. Liquid stocks only (top 10% by dollar volume)
3. Stocks that closed above their 20-day moving average.

Note: In the article, liquidity was checked. In practice, all stocks from S&P500 and IWM ETFs were used.

For the stocks that pass the screen, the bot uses intraday data to identify which stocks gapped down at least 2% below the prior day's low. 

The sell-on-gap strategy was found to be more profitable, with a Sharpe ratio of 1.30 and an annual return of 10% from 2014-2020. 

### Strategy Spark Notes
Stocks with low market cap are subject to mean reversion because less volume/liquidity requires less buy back to mean revert.
Stocks with high market cap are subject to momentum continuation because large volume/liquidity requires significant buyback to mean revert. Therefore it is more likely to continue the down trend.

Thus, on gap downs 
- Short Large Caps
- Long Small Caps

## Implementation

The bot is implemented in Python, utilizing the powerful pandas library for efficient data manipulation, and the Alpaca API for seamless trading integration.

To establish a connection to the Alpaca trading platform and execute trades, the Alpaca API is utilized. To access the API, an API Key is required, which can be obtained by signing up for a free account on the Alpaca website. This should be included in the TradingBot Class.

The Python script encompasses various functions that handle the trading strategy, leveraging pandas for data manipulation and the Alpaca API for retrieving historical data.

The TradingBot class serves as the main entry point for the bot's functionality. It initializes necessary parameters, establishes the API connection, and provides methods for retrieving historical data, filtering data based on specific criteria, identifying trading opportunities, and executing orders.

## Disclaimer

Not Financial Advice!!!

# Future Plans
- Get Historical News Data from Alpaca API
- Fine Tune Transformer (HuggingFace/OpenAI) to generate sentiment
- Use Sentiment Analysis to predict gapdowns and classify news
- Backtest Pairs Trading Strategy Based Gapdowns/GapUps predicted from Sentiment Analysis,
- How news (earnings, product launch, ...) affects historically correlated stocks

- Other Bots: Add More Strategies