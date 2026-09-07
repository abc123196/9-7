
import requests # 請求工具
from bs4 import BeautifulSoup # 解析工具
import time # 用來暫停程式

# 要爬的股票代號清單
stock = ["1101", "2330"]

for i in range(len(stock)): # 迴圈依序爬股價
    stockid = stock[i]
    
    # 組合網址
    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
    
    # 發送請求並解析 HTML
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # 定位股價
    price_tag = soup.find('span', class_=["Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)", "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)", "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"])
    
    if price_tag:
        price = price_tag.getText()
        # 回報的訊息
        message = f"股票 {stockid} 即時股價為 {price}"
        
        # Telegram Bot 設定
        token = "8205589053:AAECeDXYmQz_rwHg0Rdw0MO87FJhQUtFSJ0"
        chat_id = "6259597689"
        
        # 發送請求給 Telegram 機器人 API
        telegram_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(telegram_url)
        
    # 每次發送暫停 3 秒
    time.sleep(3)
  
