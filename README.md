# python-Task

A Flask-based API that downloads stock market OHLCV data using yfinance, validates inputs, splits date/time, resamples to any supported timeframe, and returns JSON output. It also saves the processed data as a CSV file for further analysis or automation workflows.

***How Your Project Works***

User sends request with:
symbol (AAPL)
start date
end date
timeframe (15m)
Your API downloads stock data from Yahoo using yfinance.
It splits date and time.
It resamples the data (open, high, low, close, volume).
It saves the result into a CSV file.
It returns the final data as JSON.
