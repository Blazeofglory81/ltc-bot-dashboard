import json
import os

STATE_FILE = "data/portfolio.json"

def load_portfolio():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "usd": 1000.0,
        "ltc": 0.0,
        "buy_price": None,
        "trailing_high": None
    }

def save_portfolio(portfolio):
    with open(STATE_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)