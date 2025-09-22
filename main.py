from data import stream_prices
from rsi_strategy import RSIStrategy
from ema_strategy import EMAStrategy
from datetime import datetime

print("🔄 1-MINUTE TRADING BOT STARTING...")
print("=" * 55)
print("⏰ Each analysis cycle: 1 minute")
print("💹 Timeframe: 1-minute charts")
print("📊 Strategy optimized for short-term trading")
print("=" * 55)

# ✅ Choose strategy at runtime
print("1-Minute Strategy Options:")
print("1. RSI+EMA Strategy (RSI < 35 + EMA Bullish) - More conservative")
print("2. EMA Only Strategy (Faster signals) - Recommended for 1-min")

choice = input("Select strategy (1 or 2): ").strip()

if choice == "1":
    strategy = RSIStrategy(period=10, overbought=65, oversold=35, fast_period=5, slow_period=10)
    print("✅ Using RSI+EMA Strategy (1-minute timeframe)")
    print("⏳ Needs 10 prices (10 minutes) to start...")
elif choice == "2":
    strategy = EMAStrategy(fast_period=5, slow_period=10)
    print("✅ Using EMA Strategy (1-minute timeframe)") 
    print("⏳ Needs 10 prices (10 minutes) to start...")
else:
    print("⚠️ Invalid choice, defaulting to EMA Strategy")
    strategy = EMAStrategy(fast_period=5, slow_period=10)
    print("⏳ Needs 10 prices (10 minutes) to start...")

print("=" * 55)
print("🚀 Starting 1-minute trading cycle... (Ctrl+C to stop)")
print("=" * 55)

try:
    # 1-minute intervals (60 seconds)
    for prev_price, price in stream_prices("EURUSD=X", interval=60):
        if price is None:
            continue

        signals = strategy.on_price(price)
        for sig in signals:
            current_time = datetime.now().strftime("%H:%M:%S")
            print("🎯" * 10)
            print(f"🚀 {current_time} - 1-MINUTE SIGNAL: {sig}")
            print("💡 Based on 1-minute price action")
            print("🎯" * 10)
            print()

except KeyboardInterrupt:
    print(f"\n🛑 1-minute bot stopped. Total signals: {strategy.signal_count}")
    print(f"⏰ Average signals per hour: {strategy.signal_count}")
except Exception as e:
    print(f"\n❌ Error: {e}")