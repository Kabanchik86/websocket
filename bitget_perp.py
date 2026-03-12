import asyncio
import json
import websockets
from asyncio.exceptions import CancelledError
from exel import sheet2

async def bitget_ping(ws):
    try:
        while True:
            await asyncio.sleep(30)
            await ws.send("ping")
    except asyncio.CancelledError:
        pass


async def bitget_perp(prices):
    url = "wss://ws.bitget.com/v2/ws/public"
    INSTS = []
    INSTS_SWAP = sheet2.col_values(1)[1:]
    for INST in INSTS_SWAP:
        INSTS.append(INST.replace("-USDT-SWAP", "USDT"))

    while True:
        ping_task = None
        try:
            async with websockets.connect(url, ping_interval=None) as ws:
                print("Connected_bitget_perp")

                subscribe_msg = {
                    "op": "subscribe",
                    "args": [
                        {"instType": "USDT-FUTURES", "channel": "books5", "instId": inst}
                        for inst in INSTS
                    ]
                }

                await ws.send(json.dumps(subscribe_msg))

                ping_task = asyncio.create_task(bitget_ping(ws))

                async for msg in ws:
                    # Bitget может прислать pong строкой
                    if msg == "pong":
                        # print("Got pong")
                        continue

                    inform = json.loads(msg)

                    # можно посмотреть служебные ответы
                    # print(inform)

                    if "data" not in inform or not inform["data"]:
                        continue

                    instId = inform["arg"]["instId"].replace("USDT", "-USDT-SWAP")
                    data = inform["data"][0]

                    ask = float(data["asks"][0][0])
                    bid = float(data["bids"][0][0])
                    volume_ask = float(data["asks"][0][1])
                    volume_bid = float(data["bids"][0][1])

                    prices["bitget_perp"][instId] = {
                        "ask": ask,
                        "bid": bid,
                        "ask_qty": volume_ask,
                        "bid_qty": volume_bid,
                        "ts": int(data["ts"])
                    }

        except CancelledError:
            print("Interrupted by user")
            raise

        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)

        finally:
            if ping_task:
                ping_task.cancel()
                try:
                    await ping_task
                except asyncio.CancelledError:
                    pass