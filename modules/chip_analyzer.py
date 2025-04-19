
import random

def analyze_chip(stock_code):
    """
    模擬分析法人籌碼與融資融券變化，真實版本可串接 CMoney、XQ、TWSE 資料
    回傳 dict，包含以下指標與預測建議打分因子
    """
    # 模擬資料（未來可串 API 或讀取真實資料）
    foreign_buy = random.randint(-1000, 1000)
    investment_buy = random.randint(-500, 500)
    dealer_buy = random.randint(-500, 500)
    financing_change = random.uniform(-3.0, 3.0)
    margin_change = random.uniform(-3.0, 3.0)

    # 策略邏輯（可學習強化）
    score = 0
    if foreign_buy > 0 and investment_buy > 0:
        score += 1.5
    if foreign_buy > 0 and dealer_buy > 0:
        score += 1
    if financing_change < 0 and margin_change > 0:
        score += 1.5  # 融資減/融券增 = 空單回補 → 偏多

    # 模擬三日外資連買（實際應查歷史）
    foreign_3day = all([random.randint(-200, 800) > 0 for _ in range(3)])
    if foreign_3day:
        score += 2  # 連買加分

    return {
        "foreign_buy": foreign_buy,
        "investment_buy": investment_buy,
        "dealer_buy": dealer_buy,
        "financing_change": round(financing_change, 2),
        "margin_change": round(margin_change, 2),
        "foreign_3day": foreign_3day,
        "chip_score": score
    }
