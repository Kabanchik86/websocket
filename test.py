import asyncio, json, time, requests, websockets
from asyncio.exceptions import CancelledError


# WEBSOKET BITGATE#############################################

async def bitget():
    url = "	wss://ws.bitget.com/v2/ws/public"
    INSTS = ["LABUSDT", "KGENUSDT", "RLSUSDT", "APRUSDT", "COAIUSDT"]
    while True:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print("Connected_bitget_spot")
                # Сообщение для подписки
                subscribe_msg = {
                    "op": "subscribe",
                    "args": [{"instType": "SPOT", "channel": "books5", "instId": inst} for inst in INSTS]
                }
                await ws.send(json.dumps(subscribe_msg))
                async for msg in ws:
                    # Получаем пуши
                    inform = json.loads(msg)
                    #print(inform)
                    #проверяем, что это стакан
                    if "data" not in inform or not inform["data"]:
                        continue

                    instId = inform["arg"]['instId'].replace("USDT", "-USDT")
                    data = inform["data"][0]
                    ask = float(data["asks"][0][0])
                    bid = float(data["bids"][0][0])
                    volume_ask = float(data["asks"][0][1])
                    volume_bid = float(data["bids"][0][1])

                    print(instId, ask, bid, volume_ask, volume_bid)
                    # prices["bitget"][instId] ={
                    #     "ask": ask,
                    #     "bid": bid,
                    #     "ask_qty": volume_ask,
                    #     "bid_qty": volume_bid,
                    #     "ts": int(data["ts"])
                    # }

        except CancelledError as e:
            print('Interrupted by user')
        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)

asyncio.run(bitget())