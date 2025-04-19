
import requests

def fetch_twse_realtime_data(stock_list):
    """
    stock_list: List[str]，例如 ["2330", "2324", "3037"]
    回傳格式: List[dict]，每檔股票一筆資料，包含價格、量、時間等欄位
    """
    tse_codes = [f"tse_{code}.tw" for code in stock_list]
    query = "|".join(tse_codes)
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={query}&json=1&delay=0"
    resp = requests.get(url)
    json_data = resp.json()

    if "msgArray" not in json_data:
        return []

    result = []
    for stock in json_data["msgArray"]:
        result.append({
            "stock": stock["c"],
            "name": stock["n"],
            "price": float(stock["z"]) if stock["z"] != '-' else None,
            "volume": int(stock["tv"]) if stock["tv"].isdigit() else 0,
            "total_volume": int(stock["v"]) if stock["v"].isdigit() else 0,
            "high": float(stock["h"]) if stock["h"] != '-' else None,
            "low": float(stock["l"]) if stock["l"] != '-' else None,
            "open": float(stock["o"]) if stock["o"] != '-' else None,
            "yesterday": float(stock["y"]) if stock["y"] != '-' else None,
            "time": stock["t"],
            "buy": stock["b"].split("_") if stock.get("b") else [],
            "sell": stock["a"].split("_") if stock.get("a") else [],
        })

    return result
