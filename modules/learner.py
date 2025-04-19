
import pandas as pd
import json
from collections import defaultdict

BACKTEST_FILE = "data/backtest_summary.csv"
OUTPUT_FILE = "data/learned_weights.json"

def learn_from_backtest():
    try:
        df = pd.read_csv(BACKTEST_FILE)
    except FileNotFoundError:
        return {"error": "backtest file not found"}

    # 初始化策略學習結果（後續可根據不同特徵分類）
    stats = defaultdict(lambda: {"total": 0, "success": 0})

    for _, row in df.iterrows():
        direction = row["direction"]
        result = row["strategy_success"]
        # 模擬條件關聯（可擴充為 MACD、KD 等）
        if direction == "看多":
            stats["多頭策略"]["total"] += 1
            if result == "成功":
                stats["多頭策略"]["success"] += 1
        else:
            stats["空頭策略"]["total"] += 1
            if result == "成功":
                stats["空頭策略"]["success"] += 1

    # 計算成功率與權重參數（可輸出為分數）
    weights = {}
    for k, v in stats.items():
        success_rate = v["success"] / v["total"] if v["total"] > 0 else 0
        weights[k] = {
            "success_rate": round(success_rate, 3),
            "weight": round(success_rate * 10, 2)  # 模型權重可據此使用
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(weights, f, ensure_ascii=False, indent=2)

    return weights
