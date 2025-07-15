from price_feed import get_current_price, append_price_to_history, load_price_history
from portfolio import load_portfolio, save_portfolio
from indicators import calculate_rsi
from config import BASE_BUY_AMOUNT, GAIN_TARGET, TRAILING_STOP, STOP_LOSS, RSI_PERIOD
import csv
import os
from datetime import datetime

def log_trade(action, price, amount_usd, reason=""):
    log_path = "data/trades.csv"
    exists = os.path.exists(log_path)
    with open(log_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "action", "price", "amount_usd", "reason"])
        writer.writerow([datetime.utcnow().isoformat(), action, price, amount_usd, reason])

def check_trade():
    price = get_current_price()
    append_price_to_history(price)
    history = load_price_history()
    rsi = calculate_rsi(history, RSI_PERIOD)

    if rsi is None:
        print("Waiting for enough data to calculate RSI...")
        return

    avg_price = sum(history[-15:]) / 15
    is_dip = price < avg_price * 0.98
    portfolio = load_portfolio()

    if portfolio["ltc"] == 0:
        if rsi < 30 and is_dip and portfolio["usd"] >= BASE_BUY_AMOUNT:
            buy_size = BASE_BUY_AMOUNT
            if rsi < 20:
                buy_size *= 1.5
            ltc_bought = buy_size / price
            portfolio["ltc"] = ltc_bought
            portfolio["usd"] -= buy_size
            portfolio["buy_price"] = price
            portfolio["trailing_high"] = price
            save_portfolio(portfolio)
            log_trade("BUY", price, buy_size, f"RSI={rsi:.2f}, Dip={is_dip}")
            print(f"[BUY] {ltc_bought:.4f} LTC at ${price:.2f} | RSI={rsi:.2f}")
    else:
        if price > portfolio["trailing_high"]:
            portfolio["trailing_high"] = price
            save_portfolio(portfolio)

        stop_loss_price = portfolio["buy_price"] * (1 - STOP_LOSS)
        target_price = portfolio["buy_price"] * (1 + GAIN_TARGET)
        trailing_stop_price = portfolio["trailing_high"] * (1 - TRAILING_STOP)

        if price <= stop_loss_price:
            reason = "STOP LOSS"
        elif price >= target_price and price <= trailing_stop_price:
            reason = "TRAILING EXIT"
        else:
            return

        usd_received = portfolio["ltc"] * price
        log_trade("SELL", price, usd_received, reason)
        print(f"[SELL] {portfolio['ltc']:.4f} LTC at ${price:.2f} | Reason: {reason}")
        portfolio["usd"] += usd_received
        portfolio["ltc"] = 0
        portfolio["buy_price"] = None
        portfolio["trailing_high"] = None
        save_portfolio(portfolio)