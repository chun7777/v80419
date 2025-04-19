
import requests
import pandas as pd
from io import StringIO

def fetch_twse_postclose(date_str):
    url = f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date_str}&type=ALL"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    if r.status_code != 200 or "證券代號" not in r.text:
        raise ValueError("資料抓取失敗或格式不符")

    raw_lines = r.text.splitlines()
    start = next(i for i, line in enumerate(raw_lines) if "證券代號" in line)
    csv_text = "\n".join(raw_lines[start:])
    csv_io = StringIO(csv_text)

    df = pd.read_csv(csv_io)
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns={
        "證券代號": "stock",
        "證券名稱": "name",
        "收盤價": "close",
        "開盤價": "open",
        "最高價": "high",
        "最低價": "low",
        "成交股數": "volume"
    })

    df = df[["stock", "name", "open", "high", "low", "close", "volume"]].copy()
    df["stock"] = df["stock"].astype(str)

    def clean_column(col):
        return pd.to_numeric(col.astype(str).str.replace(",", "").replace("--", ""), errors='coerce')

    df["close"] = clean_column(df["close"])
    df["open"] = clean_column(df["open"])
    df["high"] = clean_column(df["high"])
    df["low"] = clean_column(df["low"])
    df["volume"] = clean_column(df["volume"]) / 1000
    df["price"] = df["close"]
    df = df.dropna(subset=["close", "open", "high", "low", "volume"])

    return df
