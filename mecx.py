import asyncio, json, websockets, sys
sys.path.append("mexc_pb")
import PushDataV3ApiWrapper_pb2
#from google.protobuf.json_format import MessageToDict
from asyncio.exceptions import CancelledError

URL="wss://wbs-api.mexc.com/ws"
CH=["spot@public.limit.depth.v3.api.pb@TONUSDT@5", "spot@public.limit.depth.v3.api.pb@SUIUSDT@5", "spot@public.limit.depth.v3.api.pb@APTUSDT@5",
    "spot@public.limit.depth.v3.api.pb@NEARUSDT@5","spot@public.limit.depth.v3.api.pb@ATOMUSDT@5","spot@public.limit.depth.v3.api.pb@AVAXUSDT@5",
    "spot@public.limit.depth.v3.api.pb@DOTUSDT@5", "spot@public.limit.depth.v3.api.pb@UNIUSDT@5", "spot@public.limit.depth.v3.api.pb@PEPEUSDT@5"]


quote = "USDT"

async def mecx(prices):
    while True:
        try:
            async with websockets.connect(URL, ping_interval=20, ping_timeout=20) as ws:
                print("Connected_mecx")
                for ch in CH:
                    await ws.send(json.dumps({"method": "SUBSCRIPTION", "params": [ch]}))
                async for m in ws:
                    if isinstance(m, bytes):
                        w = PushDataV3ApiWrapper_pb2.PushDataV3ApiWrapper()
                        w.ParseFromString(m)
                        #print(w)
                        instId = w.symbol[:-len(quote)] + "-" + quote
                        ask = float(w.publicLimitDepths.asks[0].price)
                        bid = float(w.publicLimitDepths.bids[0].price)
                        volume_ask = float(w.publicLimitDepths.asks[0].quantity)
                        volume_bid = float(w.publicLimitDepths.bids[0].quantity)
                        ts = int(w.sendTime)

                        prices["mecx"][instId] = {
                            "ask": ask,
                            "bid": bid,
                            "ask_qty": volume_ask,
                            "bid_qty": volume_bid,
                            "ts": ts
                        }

                        #print(instId, ask, bid, volume_ask, volume_bid, ts)
        except CancelledError as e:
            print('Interrupted by user')
        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)

#asyncio.run(mecx())
