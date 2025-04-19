
from modules.live_data import fetch_twse_realtime_data

# 模擬從預測模型取得 Top 3 股票代碼（實際應由預測結果提供）
latest_top3 = ["2324", "3231", "3037"]

@app.route("/monitor")
def monitor():
    data = fetch_twse_realtime_data(latest_top3)
    return jsonify(data)

from modules.learner import learn_from_backtest

@app.route("/run_backtest")
def run_backtest_route():
    run_backtest()
    result = learn_from_backtest()
    return f"<b>✅ 回測學習已完成</b><br><pre>{result}</pre><br><a href='/'>返回首頁</a>"

from modules.post_close_data import fetch_twse_postclose
from modules.predictor import score_stocks

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("index.html")
    else:
        date_str = request.form.get("predict_date")
        df = fetch_twse_postclose(date_str)
        top3 = score_stocks(df)
        strategies = []
        for _, row in top3.iterrows():
            strategies.append({
                "stock": row["stock"],
                "name": row["name"],
                "direction": "看多" if row["macd"] > row["macd_signal"] else "看空",
                "entry": round(row["price"], 2),
                "stop_loss": round(row["price"] * 0.97, 2),
                "take_profit": round(row["price"] * 1.03, 2),
                "support": round(row["low"], 2),
                "resistance": round(row["high"], 2)
            })
        return render_template("result.html", strategies=strategies)
