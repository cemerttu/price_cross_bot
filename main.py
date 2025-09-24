# main.py - ENHANCED VERSION
from datetime import datetime
import argparse
from data import stream_prices, get_historical_data
from enhanced_strategy import EnhancedStrategy
from backtester import Backtester

def main():
    parser = argparse.ArgumentParser(description='Forex Trading Bot')
    parser.add_argument('--mode', choices=['live', 'backtest'], default='live', help='Run mode')
    parser.add_argument('--symbol', default='EURUSD=X', help='Trading symbol')
    parser.add_argument('--interval', type=int, default=1, help='Price check interval (seconds)')
    parser.add_argument('--period', default='7d', help='Historical data period for backtesting')
    
    args = parser.parse_args()
    
    SYMBOL = args.symbol
    INTERVAL = args.interval
    
    if args.mode == 'backtest':
        print("🧪 Running Backtest...")
        historical_data = get_historical_data(SYMBOL, period=args.period, interval="1m")
        
        if historical_data.empty:
            print("❌ No historical data available")
            return
            
        backtester = Backtester(initial_balance=10000.0)
        results = backtester.run_backtest(historical_data, {
            'fast_period': 13,
            'slow_period': 20,
            'rsi_period': 14
        })
        
        print(backtester.generate_report())
        
    else:  # Live trading
        strategy = EnhancedStrategy(fast_period=13, slow_period=20, rsi_period=14)
        print("🎯 Enhanced Strategy Active (EMA 13/20 + RSI 14 + Risk Management)")
        
        # Pre-load historical data
        historical_data = get_historical_data(SYMBOL, period="1d", interval="1m")
        if not historical_data.empty:
            for price in historical_data['Close'].tolist()[-100:]:  # Load more for better indicators
                strategy.prices.append(price)
        
        print(f"✅ Loaded {len(strategy.prices)} historical prices")
        print("📊 Initial Strategy Stats:")
        stats = strategy.get_strategy_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        try:
            for prev_price, price in stream_prices(SYMBOL, INTERVAL):
                signals = strategy.on_price(price)
                for s in signals:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {s}")
                
                # Print performance every 10 prices
                if len(strategy.prices) % 10 == 0:
                    stats = strategy.get_strategy_stats()
                    if stats.get('total_trades', 0) > 0:
                        print(f"📈 Equity: ${stats.get('account_balance', 0):.2f} | "
                              f"Win Rate: {stats.get('win_rate', 0):.1f}% | "
                              f"Total PnL: ${stats.get('total_pnl', 0):.2f}")
        
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped.")
            stats = strategy.get_strategy_stats()
            print("📊 Final Performance Report:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
            print("✅ All trades saved to CSV.")

if __name__ == "__main__":
    main()