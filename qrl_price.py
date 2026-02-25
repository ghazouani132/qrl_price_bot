import requests
import time
from datetime import datetime

TELEGRAM_TOKEN   = "8396116673:AAEP8q3ZClcSdU3PZXQaOp2WR34JQS3wytc"
TELEGRAM_CHAT_ID = "-1003732439601"
CHECK_EVERY      = 900  # 15 دقيقة

def send_telegram(msg):
    url = f"https://api.telegram.org/bot8396116673:AAEP8q3ZClcSdU3PZXQaOp2WR34JQS3wytc/sendMessage"
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
    print("🚀 QRL Price Bot Started!")
    while True:
        price, change = get_qrl_price()
        if price:
            emoji = "🟢" if change > 0 else "🔴"
            msg = f"""
💎 <b>QRL Price Update</b>
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💰 Price: <b>${price:.4f}</b>
{emoji} 24h Change: <b>{change:.2f}%</b>
"""
            send_telegram(msg)
            print(f"✅ Sent! QRL = ${price:.4f} | {change:.2f}%")
        time.sleep(CHECK_EVERY)

if __name__ == "__main__":
    run()