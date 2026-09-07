import requests
from bs4 import BeautifulSoup
import time

stock = ["1101", "2330"]

for i in range(len(stock)):
    stockid = stock[i]
    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    price_tag = soup.find('span', class_=["Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)", "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)", "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"])
    
    if price_tag:
        price = price_tag.getText()
        message = f"股票 {stockid} 即時股價為 {price}"
        
        token = "8205589053:AAECeDXYmQz_rwHg0Rdw0MO87FJhQUtFSJ0"
        chat_id = "6259597689"
        
        telegram_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(telegram_url)
        
    time.sleep(3)
