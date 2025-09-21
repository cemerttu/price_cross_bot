from data import stream_prices
from ema_strategy import EMAStrategy
from rsi_strategy import RSIStrategy

# ✅ Choose your strategy here
strategy = EMAStrategy(fast_period=9, slow_period=21)
strategy = RSIStrategy(period=14, overbought=70, oversold=30)

print("🔄 Starting live trading strategy... (Ctrl+C to stop)")

for prev_price, price in stream_prices("EURUSD=X", interval=10):
    if price is None:
        continue

    signals = strategy.on_price(price)
    for sig in signals:
        print(sig)
