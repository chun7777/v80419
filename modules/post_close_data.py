
import requests
import pandas as pd
from io import StringIO

def fetch_twse_postclose(date_str):
    """
    輸入：date_str = 'YYYYMMDD'，例如 '20240417'
    回傳：DataFrame，包含股票代號、名稱、成交量、收盤價等欄位
    """
    url = f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date_str}&type=ALL"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    if r.status_code != 200 or "證券代號" not in r.text:
        raise ValueError("資料抓取失敗或格式不符")

    # 清除無用行並保留包含 "證券代號" 的表格
    raw_lines = r.text.splitlines()
    start = next(i for i, line in enumerate(raw_lines) if "證券代號" in line)
    csv_text = "
".join(raw_lines[start:])
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
    df["volume"] = df["volume"].astype(str).str.replace(",", "").astype(float) / 1000
    df["close"] = df["close"].astype(str).str.replace(",", "").astype(float)
    df["open"] = df["open"].astype(str).str.replace(",", "").astype(float)
    df["high"] = df["high"].astype(str).str.replace(",", "").astype(float)
    df["low"] = df["low"].astype(str).str.replace(",", "").astype(float)
    df["price"] = df["close"]

    return df
