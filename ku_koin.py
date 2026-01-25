import asyncio, json, time, requests, websockets
from asyncio.exceptions import CancelledError

INSTS = ["TON-USDT", "SUI-USDT", "SOL-USDT", "APT-USDT", "NEAR-USDT", "ATOM-USDT", "AVAX-USDT", "DOT-USDT", "UNI-USDT", "PEPE-USDT"]

def get_bullet():
    r = requests.post("https://api.kucoin.com/api/v1/bullet-public").json()
    data = r["data"]
    server = data["instanceServers"][0]
    return data["token"], server["endpoint"], server["pingInterval"]


async def kucoin_ws(prices):
    while True:
        try:
            token, endpoint, ping_ms = get_bullet()
            ws_url = f"{endpoint}?token={token}"

            async with websockets.connect(ws_url, ping_interval=None) as ws:
                async def pinger():
                    while True:
                        await asyncio.sleep(ping_ms / 1000)
                        await ws.send(json.dumps({"id": str(int(time.time() * 1000)), "type": "ping"}))

                asyncio.create_task(pinger())
                print('Connected_kucoin')

                for inst in INSTS:
                    await ws.send(json.dumps({
                        "id": str(int(time.time() * 1000)),
                        "type": "subscribe",
                        "topic": f"/spotMarket/level2Depth5:{inst}",
                        "response": True
                    }))

                async for msg in ws:
                    # Получаем пуши
                    inform = json.loads(msg)

                    # проверяем, что это стакан
                    if "data" not in inform or not inform["data"]:
                        continue

                    instId = inform["topic"].split(":", 1)[1]
                    data = inform["data"]
                    # print(data)
                    ask = float(data["asks"][0][0])
                    bid = float(data["bids"][0][0])
                    volume_ask = float(data["asks"][0][1])
                    volume_bid = float(data["bids"][0][1])
                    prices["kucoin"][instId] = {
                        "ask": ask,
                        "bid": bid,
                        "ask_qty": volume_ask,
                        "bid_qty": volume_bid,
                        "ts": int(data["timestamp"])
                    }
                    # print(prices["kucoin"])


        except CancelledError as e:
            print('Interrupted by user')

        except Exception as e:
            print("reconnect:", e)
            await asyncio.sleep(2)

#asyncio.run(kucoin_ws())
