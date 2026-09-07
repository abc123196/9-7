import os
import time
import requests
from bs4 import BeautifulSoup

# 要爬的股票代號清單
stock_list = ["1101", "2330"]

# 從環境變數讀取 Telegram 設定
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except requests.RequestException as e:
        print(f"發送 Telegram 訊息失敗: {e}")

def get_stock_price(stockid):
    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"抓取 {stockid} 失敗: {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    price_tag = soup.find(
        "span",
        class_=[
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",
        ],
    )
    return price_tag.getText() if price_tag else None

def main():
    for stockid in stock_list:
        price = get_stock_price(stockid)
        if price:
            message = f"股票 {stockid} 即時股價為 {price}"
            send_telegram_message(message)
            print(message)
        else:
            print(f"找不到股票 {stockid} 的股價")
        time.sleep(3)  # 每次發送暫停 3 秒

if __name__ == "__main__":
    main()
