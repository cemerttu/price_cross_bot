from bot import PriceCrossBot
from data import stream_prices

bot = PriceCrossBot()

level = 1.10
lower, upper = 1.09, 1.11

print("🔄 Starting live bot... (Ctrl+C to stop)")

for prev_price, price in stream_prices("EURUSD=X", interval=10):
    if prev_price is None:
        continue

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
