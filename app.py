
from flask import Flask, render_template, request
from modules.post_close_data import fetch_twse_postclose
from modules.predictor import score_stocks

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        date_str = request.form.get("predict_date")
        print(f"🔍 收到預測日期：{date_str}")
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
    except Exception as e:
        print("❌ 預測發生錯誤：", e)
        return f"<h3>預測失敗：{e}</h3>"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
