import time
from datetime import datetime
from data import stream_prices, get_historical_data
from ema_strategy import EMAStrategy
from rsi_strategy import RSIStrategy
from indicators import get_all_indicators, get_ema_cross_signals, stochastic_oscillator

def main():
    # Configuration
    SYMBOL = "EURUSD=X"
    INTERVAL = 1  # 1-second intervals
    STRATEGY_CHOICE = "EMA"  # Choose "EMA" or "RSI"
    
    # Initialize strategy with EMA 13/20
    if STRATEGY_CHOICE.upper() == "EMA":
        strategy = EMAStrategy(fast_period=13, slow_period=20)
        print("🎯 Using EMA Strategy (13,20) with Stochastic Confirmation")
    else:
        strategy = RSIStrategy(period=14, overbought=70, oversold=30)
        print("🎯 Using RSI Strategy (14,70,30) with EMA & Stochastic Confirmation")
    
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
        price_count = 0
        last_update_time = time.time()
        
        for prev_price, current_price in stream_prices(SYMBOL, INTERVAL):
            price_count += 1
            
            # Process price through strategy
            signals = strategy.on_price(current_price, prev_price)
            
            # Print signals immediately
            for signal in signals:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] {signal}")
            
            # Print status every 30 seconds
            current_time = time.time()
            if current_time - last_update_time >= 30:
                last_update_time = current_time
                timestamp = datetime.now().strftime("%H:%M:%S")
                stats = strategy.get_strategy_stats()
                
                # Get current indicator values
                indicators = get_all_indicators(strategy.prices) if len(strategy.prices) >= 20 else {}
                stochastic_data = stochastic_oscillator(strategy.prices, k_period=14, d_period=3) if len(strategy.prices) >= 14 else {"%K": [50], "%D": [50]}
                
                stoch_k = stochastic_data["%K"][-1] if stochastic_data["%K"] else 50
                stoch_d = stochastic_data["%D"][-1] if stochastic_data["%D"] else 50
                stoch_signal = "Bullish" if stoch_k > stoch_d else "Bearish" if stoch_k < stoch_d else "Neutral"
                stoch_level = "Overbought" if stoch_k > 80 else "Oversold" if stoch_k < 20 else "Neutral"
                
                print(f"\n{'='*70}")
                print(f"📈 LIVE TRADING UPDATE [{timestamp}]")
                print(f"{'='*70}")
                print(f"💰 Current Price: {current_price:.5f}")
                
                if indicators and "error" not in indicators:
                    print(f"📊 EMA13: {indicators.get('ema_fast_13', 0):.5f}")
                    print(f"📊 EMA20: {indicators.get('ema_slow_20', 0):.5f}")
                    print(f"📈 EMA Signal: {indicators.get('ema_signal', 'calculating...')}")
                    print(f"📊 RSI: {indicators.get('rsi', 0):.1f}")
                    print(f"🎯 Stochastic: K={stoch_k:.1f}, D={stoch_d:.1f} ({stoch_signal}, {stoch_level})")
                    print(f"📈 MACD: {indicators.get('macd', 0):.5f}")
                
                print(f"⚡ Position: {stats['current_position'] or 'FLAT'}")
                if stats['current_position']:
                    print(f"📥 Entry Price: {stats['open_entry_price']:.5f}")
                    unrealized_pnl = current_price - stats['open_entry_price'] if stats['current_position'] == 'LONG' else stats['open_entry_price'] - current_price
                    pnl_color = "🟢" if unrealized_pnl > 0 else "🔴"
                    print(f"📊 Unrealized PnL: {pnl_color} {unrealized_pnl:.5f}")
                
                print(f"\n📊 PERFORMANCE SUMMARY:")
                print(f"✅ Total Trades: {stats['total_trades']}")
                print(f"✅ Wins: {stats['wins']} | ❌ Losses: {stats['losses']}")
                print(f"🎯 Win Rate: {stats['win_rate']}")
                print(f"💵 Net Profit: {stats['net_profit']:.5f}")
                print(f"📉 Max Drawdown: {stats['max_drawdown']:.5f}")
                print(f"📈 Prices Processed: {stats['data_points']}")
                print(f"{'='*70}\n")
                
    except KeyboardInterrupt:
        print(f"\n\n🛑 Trading bot stopped by user.")
        
        # Final statistics
        stats = strategy.get_strategy_stats()
        print(f"\n{'='*70}")
        print(f"📊 FINAL TRADING REPORT")
        print(f"{'='*70}")
        print(f"🎯 Strategy: EMA(13,20) with Stochastic Oscillator")
        print(f"✅ Total Trades: {stats['total_trades']}")
        print(f"✅ Wins: {stats['wins']} | ❌ Losses: {stats['losses']}")
        print(f"🎯 Win Rate: {stats['win_rate']}")
        print(f"💰 Net Profit: {stats['net_profit']:.5f}")
        print(f"📉 Max Drawdown: {stats['max_drawdown']:.5f}")
        print(f"📈 Prices Processed: {stats['data_points']}")
        print(f"⚡ Final Position: {stats['current_position'] or 'FLAT'}")
        
        # Show recent trades
        if stats['trade_details']:
            print(f"\n📋 Last 5 Trades:")
            for trade in stats['trade_details'][-5:]:
                pnl_color = "🟢" if trade['pnl'] > 0 else "🔴"
                print(f"   {pnl_color} {trade['type']}: Entry {trade['entry_price']:.5f} -> Exit {trade['exit_price']:.5f} | PnL: {trade['pnl']:.5f}")
        
        print(f"{'='*70}")
        
    except Exception as e:
        print(f"\n❌ Error in main loop: {e}")

if __name__ == "__main__":
    main()