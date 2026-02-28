import requests
import time
import os

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_EVERY      = 900  # 15 دقيقة

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in Railway Variables")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }, timeout=15)

    print("Telegram status:", resp.status_code)
    print("Telegram response:", resp.text)

def get_qrl_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=quantum-resistant-ledger&vs_currencies=usd"
        r = requests.get(url, timeout=15).json()
        return r["quantum-resistant-ledger"]["usd"]
    except Exception as e:
        print(f"Error: {e}")
        return None

def run():
    print("Bot Started")
    previous_price = None

    while True:
        price = get_qrl_price()

        if price is not None:
            if previous_price is None:
                arrow = ""
                percent_change = 0.0
            else:
                percent_change = ((price - previous_price) / previous_price) * 100
                if percent_change > 0:
                    arrow = "↑"
                elif percent_change < 0:
                    arrow = "↓"
                else:
                    arrow = ""

            # إذا ما في سهم، لا نضع فراغ زائد
            if arrow:
                msg = f"${price:.4f}\n{arrow} {percent_change:+.2f}%"
            else:
                msg = f"${price:.4f}\n{percent_change:+.2f}%"

            send_telegram(msg)
            print("Sent:", msg)

            previous_price = price

        time.sleep(CHECK_EVERY)

if __name__ == "__main__":
    run()
