import asyncio, json, websockets
from asyncio.exceptions import CancelledError

URL = "wss://contract.mexc.com/edge"
SYMBOLS = ["FLR_USDT","SUI_USDT","APT_USDT","NEAR_USDT","ATOM_USDT","AVAX_USDT","DOT_USDT","UNI_USDT","PEPE_USDT"
           ,"JUP_USDT","PENGU_USDT","RENDER_USDT","TRUMPOFFICIAL_USDT", "TONCOIN_USDT"]

bids = {}
asks = {}
last_ts = {}
last_version = {}


# функция отправки пинга
async def mexc_ping(ws):
    while True:
        await asyncio.sleep(15)  # 10–20 сек по доке MEXC
        await ws.send(json.dumps({"method": "ping"}))
# подписка на инстркументы
async def subscribe_all(ws):
    for s in SYMBOLS:
        await ws.send(json.dumps({"method": "sub.depth", "param": {"symbol": s}}))
# подписка при реконекте
async def resubscribe_one(ws, symbol):
    await ws.send(json.dumps({"method": "sub.depth", "param": {"symbol": symbol}}))

# функция обработки стакана
def apply(updates, book):
    for price, qty, *_ in updates:  # *_ игнорируем count
        price = float(price)
        qty = float(qty)
        if qty == 0:
            book.pop(price, None)
        else:
            book[price] = qty

# websocket connect
async def mecx():
    while True:
        try:
            async with websockets.connect(URL, ping_interval=None, ping_timeout=None) as ws:
                print("Connected_mecx")
                # 🔥 ВАЖНО: очистить старые данные после реконнекта
                bids.clear()
                asks.clear()
                last_ts.clear()
                last_version.clear()

                await subscribe_all(ws)

                ping_task = asyncio.create_task(mexc_ping(ws))

                try:
                    async for msg in ws:
                        data = json.loads(msg)
                        #print(data)

                        # ✅ фильтруем только стакан
                        if data.get("channel") != "push.depth":
                            continue
                        # ✅ получаем symbol, instId
                        symbol = data.get("symbol")
                        if not symbol:
                            continue
                        instId = symbol.replace("_", "-").replace("COIN", "").replace("ECOIN", "").replace("OFFICIAL", "")

                        # ✅ bids/asks внутри data["data"], versions
                        ob = data.get("data", {})

                        if instId not in last_version:
                            last_version[instId] = None

                        version = ob.get('version')
                        begin = ob.get('begin')

                        # обработка версионности
                        if begin is not None and last_version[instId] is not None:
                            if begin > last_version[instId] + 1:
                                print("Missed updates for", instId, "-> resubscribe")
                                bids.get(instId, {}).clear()
                                asks.get(instId, {}).clear()
                                last_ts[instId] = None
                                last_version[instId] = None
                                await resubscribe_one(ws, symbol)
                                continue

                        # инициализация instId
                        if instId not in bids:
                            bids[instId] = {}
                            asks[instId] = {}
                            last_ts[instId] = None
                            last_version[instId] = version

                        apply(ob.get("bids", []), bids[instId])
                        apply(ob.get("asks", []), asks[instId])
                        ts = int(data.get('ts'))

                        last_ts[instId] = ts
                        last_version[instId] = version  # <-- ВАЖНО: обновляем

                        # if bids[instId] and asks[instId]:
                        #     best_bid_p = max(bids[instId])
                        #     best_ask_p = min(asks[instId])
                        #     best_bid_q = bids[instId][best_bid_p]
                        #     best_ask_q = asks[instId][best_ask_p]
                        #     prices["mecx"][instId] = {
                        #         "ask": best_ask_p,
                        #         "bid": best_bid_p,
                        #         "ask_qty": best_ask_q,
                        #         "bid_qty": best_bid_q,
                        #         "ts": ts
                        #     }

                        if bids[instId] and asks[instId]:
                            best_bid_p = max(bids[instId])
                            best_ask_p = min(asks[instId])
                            best_bid_q = bids[instId][best_bid_p]
                            best_ask_q = asks[instId][best_ask_p]
                            print(instId, "TOP1:", best_bid_p, best_bid_q, "|", best_ask_p, best_ask_q)

                finally:
                    ping_task.cancel()

        except CancelledError:
            print('Interrupted by user')
            raise
        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)


asyncio.run(mecx())
