import requests
import csv
import os
from config import SYMBOL, HISTORY_FILE, MAX_HISTORY

def get_current_price():
    url = f"https://api.coinbase.com/v2/prices/{SYMBOL}/spot"
    resp = requests.get(url)
    data = resp.json()
    return float(data['data']['amount'])

def append_price_to_history(price):
    history = load_price_history()
    history.append(price)
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    with open(HISTORY_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        for p in history:
            writer.writerow([p])

def load_price_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            reader = csv.reader(f)
            return [float(row[0]) for row in reader if row]
    except:
        return []