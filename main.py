from datetime import datetime
from data import stream_prices, get_historical_data
from ema_strategy import EMAStrategy

def main():
    SYMBOL = "EURUSD=X"
    INTERVAL = 1  # seconds
    STRATEGY_CHOICE = "EMA"

    strategy = EMAStrategy(fast_period=13, slow_period=20)
    print("🎯 Using EMA Strategy (13,20)")

    historical_data = get_historical_data(SYMBOL, period="1d", interval="1m")
    if not historical_data.empty:
        for price in historical_data['Close'].tolist()[-50:]:
            strategy.prices.append(price)

    try:
        for prev_price, price in stream_prices(SYMBOL, INTERVAL):
            signals = strategy.on_price(price)
            for s in signals:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {s}")

    except KeyboardInterrupt:
        print("\n🛑 Bot stopped.")
        stats = strategy.get_strategy_stats()
        print(f"Total signals: {stats['total_signals']}")
        print(f"Final position: {stats['current_position']}")
        print("✅ All trades saved to CSV.")

if __name__ == "__main__":
    main()
