import os
import requests
import time

TELEGRAM_TOKEN = "8396116673:AAEP8q3ZClcSdU3PZXQaOp2WR34JQS3wytc"
TELEGRAM_CHAT_ID = "-1003732439601" CHECK_EVERY = 900 # 15 دقيقة
def send_telegram(msg): url = f"https://api.telegram.org/bot8396116673:AAEP8q3ZClcSdU3PZXQaOp2WR34JQS3wytc/sendMessage" 
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})

def get_qrl_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-quantum-resistant-ledger&vs_currencies=usd&include_24hr_change=true"
    r = requests.get(url, timeout=20).json()
    price = r["the-quantum-resistant-ledger"]["usd"]
    change = r["the-quantum-resistant-ledger"]["usd_24h_change"]
    return price, change

def run():
    while True:
        try:
            price, change = get_qrl_price()
            msg = f"{price:.4f}\n{change:.2f}%"
            send_telegram(msg)
        except Exception as e:
            print("Error:", e)
        time.sleep(CHECK_EVERY)

if __name__ == "__main__":
    run()


