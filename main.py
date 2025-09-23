import time
from datetime import datetime
from data import stream_prices, get_historical_data
from ema_strategy import EMAStrategy
from rsi_strategy import RSIStrategy
from indicators import get_all_indicators

def main():
    # Configuration
    SYMBOL = "EURUSD=X"
    INTERVAL = 1  # 1-second intervals
    STRATEGY_CHOICE = "EMA"  # Choose "EMA" or "RSI"
    
    # Initialize strategy
    if STRATEGY_CHOICE.upper() == "EMA":
        strategy = EMAStrategy(fast_period=12, slow_period=26)
        print("🎯 Using EMA Strategy (12,26)")
    else:
        strategy = RSIStrategy(period=14, overbought=70, oversold=30)
        print("🎯 Using RSI Strategy (14,70,30)")
    
    print(f"🚀 Starting High-Frequency Trading Bot")
    print(f"📈 Symbol: {SYMBOL}")
    print(f"⏱️  Interval: {INTERVAL} second(s)")
    print(f"📊 Data collection and analysis active...")
    print("Press Ctrl+C to stop\n")
    
    # Get some initial historical data for better indicator calculation
    print("📥 Loading initial historical data...")
    historical_data = get_historical_data(SYMBOL, period="1d", interval="1m")
    if historical_data is not None:
        initial_prices = historical_data['Close'].tolist()[-50:]  # Last 50 prices
        for price in initial_prices:
            strategy.prices.append(price)
        print(f"✅ Loaded {len(initial_prices)} historical prices")
    
    try:
        signal_count = 0
        price_count = 0
        
        for prev_price, current_price in stream_prices(SYMBOL, INTERVAL):
            price_count += 1
            
            # Process price through strategy
            signals = strategy.on_price(current_price, prev_price)
            
            # Print signals immediately
            for signal in signals:
                signal_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] {signal}")
            
            # Print status every 30 seconds
            if price_count % 30 == 0:
                timestamp = datetime.now().strftime("%H:%M:%S")
                stats = strategy.get_strategy_stats()
                print(f"\n📈 Status Update [{timestamp}]")
                print(f"💰 Current Price: {current_price:.5f}")
                print(f"📊 Prices Collected: {stats['data_points']}")
                print(f"🎯 Signals Generated: {stats['total_signals']}")
                print(f"⚡ Current Position: {stats['current_position'] or 'None'}")
                
                # Show indicator values if we have enough data
                if len(strategy.prices) >= 26:
                    indicators = get_all_indicators(strategy.prices)
                    print(f"📊 RSI: {indicators.get('rsi', 0):.2f}")
                    print(f"📊 EMA12: {indicators.get('ema_12', 0):.5f}")
                    print(f"📊 EMA26: {indicators.get('ema_26', 0):.5f}")
                print()
                
    except KeyboardInterrupt:
        print(f"\n\n🛑 Trading bot stopped by user.")
        
        # Final statistics
        stats = strategy.get_strategy_stats()
        print("\n📊 FINAL STATISTICS:")
        print(f"Total prices processed: {stats['data_points']}")
        print(f"Total signals generated: {stats['total_signals']}")
        print(f"Final position: {stats['current_position']}")
        
    except Exception as e:
        print(f"\n❌ Error in main loop: {e}")

if __name__ == "__main__":
    main()
