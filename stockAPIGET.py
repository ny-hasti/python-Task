# ============================================
# Stock Data Downloader & Resampler API
# Using Flask + yfinance + pandas
# ============================================

from flask import Flask, request, jsonify
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# allowed timeframe
VALID_INTERVALS = [
    '1m','2m','5m','15m','30m','60m','90m',
    '1h','1d','5d','1wk','1mo','3mo'
]

@app.route('/dowget', methods=['GET'])
def download_stock():

    try:
        # -------- Read GET parameters --------
        symbol = request.args.get("symbol")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        timeframe = request.args.get("timeframe")

        if not all([symbol, start_date, end_date, timeframe]):
            return jsonify({"error": "Missing required GET parameters"}), 400

        # -------- Validate --------
        if timeframe not in VALID_INTERVALS:
            return jsonify({"error": "Invalid timeframe"}), 400

        # -------- Download data --------
        stock = yf.download(
            tickers=symbol,
            start=start_date,
            end=end_date,
            interval=timeframe,
            progress=False
        )

        if stock.empty:
            return jsonify({"error": "No data found"}), 400

        stock.reset_index(inplace=True)

        datetime_col = 'Datetime' if 'Datetime' in stock.columns else 'Date'

        # -------- split date & time --------
        stock['date'] = pd.to_datetime(stock[datetime_col]).dt.date
        stock['time'] = pd.to_datetime(stock[datetime_col]).dt.time

        stock = stock[['date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume']]
        stock.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']

        stock.dropna(inplace=True)

        # -------- Resample --------
        stock['datetime'] = pd.to_datetime(stock['date'].astype(str) + ' ' + stock['time'].astype(str))
        stock.set_index('datetime', inplace=True)

        resampled = stock.resample(timeframe).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        # Add date/time back
        resampled['date'] = resampled.index.date.astype(str)
        resampled['time'] = resampled.index.time.astype(str)

        resampled = resampled[['date','time','open','high','low','close','volume']]

        # -------- Save CSV --------
        filename = f"{symbol}_{timeframe}.csv"
        resampled.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

        return jsonify({
            "message": "Data downloaded successfully",
            "filename": filename,
            "rows": len(resampled),
            "data": resampled.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5004, debug=True)
