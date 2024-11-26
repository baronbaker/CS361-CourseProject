from flask import Flask, jsonify, request
from datetime import datetime
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route('/avg-volume', methods=['GET'])
def avg_volume():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # check for ticker
    if not ticker:
        return jsonify({"error": "Error: ticker required"}), 400

    #Check for start and end date
    if not start_date or not end_date:
        return jsonify({"error": "Error: Start and End date are required"}), 400
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Error: Format as YYYY-MM-DD"}), 400

    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        return jsonify({"error": "Error: no data found."}), 400

    #calculate average volume
    average_volume = data['Volume'].mean()
    if isinstance(average_volume, pd.Series):
        average_volume = average_volume.item()

    return jsonify({
        "ticker": ticker,
        "average_volume": average_volume,
        "message": "Success"
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1234)
