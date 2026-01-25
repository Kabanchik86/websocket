from pybit.unified_trading import WebSocket
import asyncio
from time import sleep

INSTS = ["TONUSDT", "SUIUSDT", "APTUSDT", "NEARUSDT", "ATOMUSDT", "AVAXUSDT", "DOTUSDT", "UNIUSDT", "PEPEUSDT"]
quote = "USDT"

async def buy_bit(prices):
    ws = WebSocket(
        testnet=False,
        channel_type="spot",
    )
    print("Connected_buy_bit")

    def handle_message(message):
        data = message['data']
        # Достаем ask, bid, voluem...
        if data['a'] and data['b']:
            ask = float(data['a'][0][0])
            bid = float(data['b'][0][0])
            volume_ask = float(data['a'][0][1])
            volume_bid = float(data['b'][0][1])
            instId = data['s'][:-len(quote)] + "-" + quote
            ts = int(message['ts'])

            prices["buy_bit"][instId] = {
                "ask": ask,
                "bid": bid,
                "ask_qty": volume_ask,
                "bid_qty": volume_bid,
                "ts": ts
            }
        #print(ask, bid, volume_ask, volume_bid, instId, ts)


    for inst in INSTS:
        ws.orderbook_stream(
            depth=1,
            symbol=inst,
            callback=handle_message
            )

    await asyncio.Event().wait()

