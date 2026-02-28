import requests
import time
from datetime import datetime

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_EVERY      = 900

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})

def get_qrl_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=quantum-resistant-ledger&vs_currencies=usd&include_24hr_change=true"
        r   = requests.get(url).json()
        price  = r["quantum-resistant-ledger"]["usd"]
        change = r["quantum-resistant-ledger"]["usd_24h_change"]
        return price, change
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def run():
    print("Bot Started")
    while True:
        price, change = get_qrl_price()
        if price is not None:
            msg = f"${price:.4f}\n{change:.2f}%"
            send_telegram(msg)
            print("Sent:", msg)
        time.sleep(CHECK_EVERY)

if __name__ == "__main__":
    run()

