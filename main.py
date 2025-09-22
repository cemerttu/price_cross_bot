import time
from data import stream_prices
from rsi_strategy import RSIStrategy
from ema_strategy import EMAStrategy

print("🔄 Trading Bot Starting...")

# ✅ Choose strategy at runtime
choice = input("Select strategy (1=RSI+EMA, 2=EMA only): ").strip()

if choice == "1":
    strategy = RSIStrategy(period=14, overbought=70, oversold=30)
    print("✅ Using RSI+EMA Strategy")
elif choice == "2":
    strategy = EMAStrategy(fast_period=9, slow_period=21)
    print("✅ Using EMA Strategy")
else:
    print("⚠️ Invalid choice, defaulting to RSI+EMA Strategy")
    strategy = RSIStrategy(period=14, overbought=70, oversold=30)

print("🔄 Running strategy (prints signals every 1 minute)... (Ctrl+C to stop)")

last_print_time = 0
duration = 60  # 1 minute in seconds

for prev_price, price in stream_prices("EURUSD=X", interval=3):  # fetch every 3 sec
    if price is None:
        continue

    signals = strategy.on_price(price)

    # Only print signals once every 60 seconds
    if time.time() - last_print_time >= duration:
        for sig in signals:
            print(sig)
        last_print_time = time.time()
