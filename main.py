from bot import PriceCrossBot
from data import stream_prices
import yfinance as yf

# Initialize bot
bot = PriceCrossBot()

# Set your levels
level = 1.10
lower, upper = 1.09, 1.11

# Load history once (for RSI/EMA/ATR filters)
df = yf.download("EURUSD=X", period="5d", interval="1m")
prices = df["Close"].tolist()
highs = df["High"].tolist()
lows = df["Low"].tolist()

print("🔄 Starting live bot... (Ctrl+C to stop)")

# Live loop
for prev_price, price in stream_prices("EURUSD=X", interval=10):
    if prev_price is None:
        continue

    # --- Your original checks ---
    if bot.crossing_up(prev_price, price, level):
        print(f"📈 Crossing UP {level} (Price: {price})")

    if bot.crossing_down(prev_price, price, level):
        print(f"📉 Crossing DOWN {level} (Price: {price})")

    if bot.entering_channel(prev_price, price, lower, upper):
        print(f"➡️ Entering Channel {lower}-{upper} (Price: {price})")

    if bot.exiting_channel(prev_price, price, lower, upper):
        print(f"⬅️ Exiting Channel {lower}-{upper} (Price: {price})")

    if bot.moving_up(prev_price, price):
        print(f"⬆️ Moving Up: {prev_price} → {price}")

    if bot.moving_down(prev_price, price):
        print(f"⬇️ Moving Down: {prev_price} → {price}")

    # --- New accuracy filters ---
    if bot.confirmed_crossing_up(prev_price, price, level, prices, highs, lows):
        print(f"✅ Strong Crossing UP confirmed (Price: {price})")

    if bot.confirmed_crossing_down(prev_price, price, level, prices, highs, lows):
        print(f"✅ Strong Crossing DOWN confirmed (Price: {price})")

    # Update history with new live candle
    prices.append(price)
    highs.append(price)  # ideally update with real high of candle
    lows.append(price)   # ideally update with real low of candle
