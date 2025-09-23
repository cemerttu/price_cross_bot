from datetime import datetime
from ema_strategy import EMAStrategy
from rsi_strategy import RSIStrategy
from data import load_csv_prices, get_historical_data, stream_prices
from indicators import get_all_indicators

def main():
    SYMBOL = "EURUSD=X"
    INTERVAL = 1          # 1-second
    STRATEGY_CHOICE = "EMA"  # "EMA" or "RSI"
    USE_CSV = True
    CSV_FILE = "EURUSD_1min.csv"

    # Initialize strategy
    strategy = EMAStrategy(fast_period=5, slow_period=10) if STRATEGY_CHOICE.upper() == "EMA" else RSIStrategy()
    print(f"🎯 Using {STRATEGY_CHOICE.upper()} Strategy")

    # Load prices
    if USE_CSV:
        csv_prices = load_csv_prices(CSV_FILE)
        if csv_prices:
            for p in csv_prices:
                strategy.prices.append(p)
            print(f"✅ Loaded {len(csv_prices)} prices from CSV")
    else:
        hist = get_historical_data(SYMBOL, period="1d", interval="1m")
        if hist is not None:
            for p in hist['Close'].tolist()[-50:]:
                strategy.prices.append(p)
            print(f"✅ Loaded {len(strategy.prices)} prices from Yahoo")

    # Run backtest or live stream
    try:
        if USE_CSV and csv_prices:
            print("📊 Running backtest on CSV...")
            for i in range(1, len(csv_prices)):
                prev_price = csv_prices[i-1]
                current_price = csv_prices[i]
                signals = strategy.on_price(current_price, prev_price)
                for s in signals:
                    print(f"[{i}] {s}")
            print("✅ Backtest complete")
        else:
            print("🚀 Starting live streaming...")
            for prev_price, price in stream_prices(SYMBOL, INTERVAL):
                signals = strategy.on_price(price, prev_price)
                for s in signals:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] {s}")
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
    finally:
        stats = strategy.get_strategy_stats()
        print(f"\n📊 FINAL STATS: {stats}")

if __name__ == "__main__":
    main()
