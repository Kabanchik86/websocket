import asyncio, json, websockets, sys
sys.path.append("mexc_pb")
import PushDataV3ApiWrapper_pb2
#from google.protobuf.json_format import MessageToDict
from asyncio.exceptions import CancelledError

URL="wss://wbs-api.mexc.com/ws"
CH="spot@public.limit.depth.v3.api.pb@BTCUSDT@5"

async def main():
    while True:
        try:
            async with websockets.connect(URL) as ws:
                await ws.send(json.dumps({"method":"SUBSCRIPTION","params":[CH]}))
                async for m in ws:
                    if isinstance(m, bytes):
                        w = PushDataV3ApiWrapper_pb2.PushDataV3ApiWrapper()
                        w.ParseFromString(m)
                        print(w)
                        #print(MessageToDict(w.publicLimitDepths, preserving_proto_field_name=True))
        except CancelledError as e:
            print('Interrupted by user')
        except Exception as e:
            print(f"Reconnect after error: {type(e).__name__}: {e}")
            await asyncio.sleep(2)

asyncio.run(main())
