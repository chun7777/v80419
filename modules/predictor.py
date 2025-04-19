
import pandas as pd
import json
from ta.momentum import stoch, stoch_signal
from ta.trend import macd, macd_signal
from modules.structure_analyzer import detect_structures
from modules.chip_analyzer import analyze_chip
from modules.price_structure import detect_bollinger_breakout

def enrich_technical(df):
    df["kd_k"] = stoch(df["high"], df["low"], df["price"])
    df["kd_d"] = stoch_signal(df["high"], df["low"], df["price"])
    df["macd"] = macd(df["price"])
    df["macd_signal"] = macd_signal(df["price"])
    df["ma20"] = df["price"].rolling(window=20).mean()
    return df

def load_weights():
    try:
        with open("data/learned_weights.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def score_stocks(df):
    df = enrich_technical(df)
    weights = load_weights()
    wt_long = weights.get("多頭策略", {}).get("weight", 5)
    wt_short = weights.get("空頭策略", {}).get("weight", 5)

    score = []
    for i in range(len(df)):
        row = df.iloc[i]
        s = 0
        if row["volume"] > 5000:
            s += 2
        if row["price"] < 150:
            s += 1
        if row["macd"] > row["macd_signal"]:
            s += wt_long / 2
        if row["kd_k"] < row["kd_d"]:
            s -= 10 - (wt_short / 2)

        struct_result = detect_structures(df.iloc[max(i - 2, 0):i + 1].copy())
        if struct_result.get("fvg_bullish"): s += 1.5
        if struct_result.get("ma_breakout"): s += 1.5
        if struct_result.get("false_break_support"): s += 1
        if struct_result.get("liquidity_sweep"): s += 1

        chip_result = analyze_chip(str(int(row["stock"])) if "stock" in row else "2330")
        s += chip_result["chip_score"]

        # 加入布林通道突破判斷
        breakout_result = detect_bollinger_breakout(df.iloc[max(i - 20, 0):i + 1].copy())
        if breakout_result["break_upper"]:
            s += 1.5  # 強勢上攻加分
        if breakout_result["break_lower"]:
            s -= 1.0  # 跌破布林下緣偏弱警訊

        df.at[i, "structure_score"] = s
        df.at[i, "chip_score"] = chip_result["chip_score"]
        score.append(s)

    df["score"] = score
    return df.sort_values("score", ascending=False).head(3)
