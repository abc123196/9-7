import os
import time
import requests
from bs4 import BeautifulSoup

stock_list = ["1101", "2330"]

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.get(url, params={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"Telegram 回應: {r.status_code} {r.text}")
    except requests.RequestException as e:
        print(f"發送 Telegram 訊息失敗: {e}")

def get_stock_price(stockid):
    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=10,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"抓取 {stockid} 失敗: {e}")
        return None

    print(f"{stockid} 網頁狀態碼: {r.status_code}, 內容長度: {len(r.text)}")

    soup = BeautifulSoup(r.text, "html.parser")
    price_tag = soup.find(
        "span",
        class_=[
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",
        ],
    )

    if not price_tag:
        print(f"{stockid} 找不到 price_tag，可能是 class 名稱已改版")
        # 印出前 500 字元幫助排查
        print(r.text[:500])

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
        time.sleep(3)

if __name__ == "__main__":
    main()
