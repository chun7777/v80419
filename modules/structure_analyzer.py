
import pandas as pd

def detect_structures(df):
    """
    輸入：包含開/高/低/收/均線的 DataFrame（單一股票多日）
    輸出：dict, 包含各種 ICT 結構判斷結果
    """
    result = {
        "fvg_bullish": False,
        "ma_breakout": False,
        "false_break_support": False,
        "liquidity_sweep": False
    }

    if len(df) < 3:
        return result

    # FVG 判斷（今日低 > 昨日高）
    if df.iloc[-1]["low"] > df.iloc[-2]["high"]:
        result["fvg_bullish"] = True

    # 均線突破（站上 20MA）
    if df.iloc[-1]["close"] > df.iloc[-1]["ma20"] and df.iloc[-2]["close"] <= df.iloc[-2]["ma20"]:
        result["ma_breakout"] = True

    # 假跌破支撐（跌破昨日低點後收高）
    if df.iloc[-1]["low"] < df.iloc[-2]["low"] and df.iloc[-1]["close"] > df.iloc[-2]["low"]:
        result["false_break_support"] = True

    # 流動性掃過（當日下影線超長）
    tail = df.iloc[-1]["close"] - df.iloc[-1]["low"]
    body = abs(df.iloc[-1]["close"] - df.iloc[-1]["open"])
    if tail > body * 2:
        result["liquidity_sweep"] = True

    return result
