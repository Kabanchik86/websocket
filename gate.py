import time, asyncio, websockets, json
from asyncio.exceptions import CancelledError

bids = {}
asks = {}
last_update = {}
last_ts = {}


#INSTS = ["FLR_USDT"]

INSTS = ["FLR_USDT","SUI_USDT","APT_USDT","NEAR_USDT","ATOM_USDT","AVAX_USDT","DOT_USDT","UNI_USDT","PEPE_USDT"
            ,"JUP_USDT","PENGU_USDT","RENDER_USDT","TRUMP_USDT", "TON_USDT", "FIL-USDT"]

def apply(updates, book):
    for price, qty in updates:
        price = float(price)
        qty = float(qty)
        if qty == 0:
            book.pop(price, None)
        else:
            book[price] = qty

async def gate(prices):
    url = "wss://api.gateio.ws/ws/v4/"

    while True:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print("Connected_gate")

                for inst in INSTS:
                    await ws.send(json.dumps({
                        "time": int(time.time()),
                        "channel": "spot.obu",
                        "event": "subscribe",
                        "payload": [f"ob.{inst}.50"]
                    }))

                async for msg in ws:
                    try:
                        inform = json.loads(msg)
                    except json.JSONDecodeError:
                        continue

                    #print(inform)

                    ev = inform.get("event")  # <-- вместо inform["event"]
                    if ev == "subscribe":
                        continue
                    if ev != "all" and ev != "update":
                        continue

                    ob = inform.get("result")
                    if not isinstance(ob, dict):
                        continue

                    s = ob.get("s")
                    if not s:
                        continue

                    instId = s.replace("ob.", "").replace("_", "-").replace(".50", "")

                    if instId not in last_update:
                        last_update[instId] = None

                    u = ob.get("u")
                    U = ob.get("U")

                    if instId not in bids:
                        bids[instId] = {}
                        asks[instId] = {}
                        last_update[instId] = u
                        last_ts[instId] = None

                    # SNAPSHOT
                    is_snapshot = (ob.get("full") is True)

                    # SNAPSHOT (full=True приходит с event="update")
                    if is_snapshot:
                        bids[instId].clear()
                        asks[instId].clear()

                        apply(ob.get("b", []), bids[instId])
                        apply(ob.get("a", []), asks[instId])

                        ts = ob.get("t")
                        last_ts[instId] = ts

                        if u is not None:
                            last_update[instId] = u

                    # UPDATES
                    else:
                        if u is not None and U is not None:
                            prev = last_update[instId]
                            if prev is not None and prev != U - 1:
                                print("Missed updates for", instId, f"(prev={prev}, U={U}, u={u}) -> reconnect")

                                bids[instId].clear()
                                asks[instId].clear()
                                last_update[instId] = None

                                await ws.close()
                                break

                        apply(ob.get("b", []), bids[instId])
                        apply(ob.get("a", []), asks[instId])
                        ts = ob.get("t")
                        last_ts[instId] = ts

                        if u is not None:
                            last_update[instId] = u

                    if bids[instId] and asks[instId]:
                        best_bid_p = max(bids[instId])
                        best_ask_p = min(asks[instId])
                        best_bid_q = bids[instId][best_bid_p]
                        best_ask_q = asks[instId][best_ask_p]
                        tm = last_ts[instId]
                        prices["gate"][instId] = {
                            "ask": best_ask_p,
                            "bid": best_bid_p,
                            "ask_qty": best_ask_q,
                            "bid_qty": best_bid_q,
                            "ts": tm
                        }
                        #print(instId, "TOP1:", best_bid_p, best_bid_q, "|", best_ask_p, best_ask_q, "|", tm)

        except CancelledError:
            print('Interrupted by user')
            break
        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)

# asyncio.run(gate())