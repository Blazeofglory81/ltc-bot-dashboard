import time
from trade_logic import check_trade
from config import POLL_INTERVAL

print("Starting Local-History LTC Bot (Paper Mode)...")

while True:
    try:
        check_trade()
    except Exception as e:
        print("Error:", e)
    time.sleep(POLL_INTERVAL)