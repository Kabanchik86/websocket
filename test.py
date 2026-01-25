from pybit.unified_trading import WebSocket
import asyncio
from time import sleep

INSTS = ["TONUSDT", "SUIUSDT", "APTUSDT", "NEARUSDT", "ATOMUSDT", "AVAXUSDT", "DOTUSDT", "UNIUSDT", 'PEPEUSDT']
quote = "USDT"


async def byu_bit():
    ws = WebSocket(
        testnet=False,
        channel_type="spot",
    )

    def handle_message(message):
        data = message['data']
        if data['a'] and data['b']:
            ask = data['a'][0][0]
            bid = data['b'][0][0]
            volume_ask = data['a'][0][1]
            volume_bid = data['b'][0][1]
            instId = data['s'][:-len(quote)] + "-" + quote
            ts = message['ts']
            print(ask, bid, volume_ask, volume_bid, instId, ts)

    for inst in INSTS:
        ws.orderbook_stream(
            depth=1,
            symbol=inst,
            callback=handle_message
        )

    while True:
        sleep(1)


asyncio.run(byu_bit())
