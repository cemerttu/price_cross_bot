# test_pnl_guaranteed.py
import os
from enhanced_strategy import EnhancedStrategy

def test_guaranteed_pnl():
    print("🧪 GUARANTEED PnL Tracking Test")
    print("=" * 50)
    
    # Clean up previous files
    for file in ["trade_log.csv", "pnl_tracking.csv"]:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Cleaned up {file}")
    
    # Create strategy
    strategy = EnhancedStrategy()
    
    # Create realistic EUR/USD price movement
    print("\n📈 Generating realistic price data...")
    base_price = 1.18000
    prices = []
    
    # Simulate some price movement
    for i in range(50):
        # Small random walk
        import random
        movement = random.uniform(-0.0002, 0.0003)
        new_price = base_price + movement
        prices.append(new_price)
        base_price = new_price
    
    print("💰 Running strategy with price data...")
    for i, price in enumerate(prices):
        signals = strategy.on_price(price)
        if signals:
            print(f"Price {i+1}: {price:.5f} -> {signals[0]}")
    
    # Force close any remaining open trades
    if strategy.risk_manager.open_trades:
        print("\n🔒 Force closing remaining trades...")
        strategy.risk_manager.close_trade_manually(prices[-1])
    
    # Display results
    stats = strategy.get_strategy_stats()
    print("\n📊 FINAL RESULTS:")
    print("=" * 30)
    for key, value in stats.items():
        print(f"{key:20}: {value}")
    
    # Check CSV files
    print("\n📁 FILE STATUS:")
    print("=" * 30)
    for file in ["trade_log.csv", "pnl_tracking.csv"]:
        if os.path.exists(file):
            import pandas as pd
            df = pd.read_csv(file)
            print(f"✅ {file}: {len(df)} records")
            if len(df) > 0:
                print(f"   Columns: {list(df.columns)}")
                print(f"   First few rows:")
                print(df.head().to_string(index=False))
        else:
            print(f"❌ {file}: Not found")

if __name__ == "__main__":
    test_guaranteed_pnl()