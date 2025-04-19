
import pandas as pd
from ta.volatility import BollingerBands

def detect_bollinger_breakout(df):
    """
    傳入含價格的 DataFrame，回傳是否突破布林上/下軌
    """
    bb = BollingerBands(close=df["price"], window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()

    latest = df.iloc[-1]
    breakout = {
        "break_upper": latest["price"] > latest["bb_upper"],
        "break_lower": latest["price"] < latest["bb_lower"]
    }
    return breakout
