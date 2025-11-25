# python-Task

A Flask-based API that downloads stock market OHLCV data using yfinance, validates inputs, splits date/time, resamples to any supported timeframe, and returns JSON output. It also saves the processed data as a CSV file for further analysis or automation workflows.
# step

**1️. Install Required Libraries**

Run these commands in your terminal:
pip install flask yfinance pandas

**2️. Save Your Python File**

Save your code in a file named:
app.py

**3️. Run Your Flask Server**

Run:
python app.py
Your API will start on:
http://localhost:5004

# WORKING STEPS (How Your API Works)
**STEP-1 → User Sends GET Request**

User calls your API like this:
http://localhost:5004/dowget?symbol=RELIANCE.NS&start_date=2024-01-01&end_date=2024-02-01&timeframe=15m


The API expects 4 inputs:
Parameter	Meaning
symbol	Stock symbol (e.g., RELIANCE.NS)
start_date	Start date
end_date	End date
timeframe	Candle interval (must be valid)

**STEP-2 → API Validates Parameters**

The code checks:
✔ all parameters exist
✔ timeframe is valid

If anything is wrong → API returns error message.

**STEP-3 → Stock Data Download (yfinance)**

The API downloads stock data:
stock = yf.download(tickers=symbol, start=start_date, end=end_date, interval=timeframe)
If no data found → it returns error.

**STEP-4 → Date & Time Splitting**

Your code separates:
full datetime → date
full datetime → time
So final columns become:
date | time | open | high | low | close | volume

**STEP-5 → Resampling**

The API resamples candles using:

stock.resample(timeframe).agg(...)

This creates new candles such as:

5 min
15 min
30 min
1 hour
1 day
etc.

**STEP-6 → Save to CSV**

Your code creates a filename:
RELIANCE.NS_15m.csv
Then appends new rows into the file automatically.

**STEP-7 → Return JSON Output**

API returns:

message
filename
rows
full candle data

Example output:

{
  "message": "Data downloaded successfully",
  "filename": "RELIANCE.NS_15m.csv",
  "rows": 96,
  "data": [
    {"date": "...", "time": "...", "open": 1234, ... }
  ]
}
