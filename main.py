import asyncio, time
from exel import write_to_arbitrage
from okx_perp import okx_perp
from bitget_spot import bitget
from exel import sheet2
from datetime import datetime

INSTS = sheet2.col_values(1)[1:]
arbitrage_queue = asyncio.Queue(maxsize=1000)
last_signal_time = {}

prices = {
    # "okx": {inst: {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None, "local_ts": None}
    #     for inst in INSTS},
    "okx_perp": {inst: {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None, "local_ts": None}
        for inst in INSTS},
    "kucoin": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'SUI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'APT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'NEAR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'ATOM-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'AVAX-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'DOT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'UNI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'PEPE-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'RENDER-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'TRUMP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
               },
    "kucoin_perp": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'SUI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'APT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'NEAR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'ATOM-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'AVAX-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'DOT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'UNI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'PEPE-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'RENDER-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'TRUMP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               #'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
               'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
               },
    "buy_bit": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'SUI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'APT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'NEAR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'ATOM-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'AVAX-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'DOT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'UNI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'PEPE-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'RENDER-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'TRUMP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
                'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
                },
    "mecx": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'SUI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'APT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'NEAR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'ATOM-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'AVAX-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},###
             'DOT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},###
             'UNI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'PEPE-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'RENDER-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'TRUMP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
             },
    "gate_perp": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'SUI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'APT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'NEAR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'ATOM-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'AVAX-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},  ###
             'DOT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},  ###
             'UNI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'PEPE-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'RENDER-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'TRUMP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
             },
    "gate": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'SUI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'APT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'NEAR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'ATOM-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'AVAX-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},  ###
            'DOT-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},  ###
            'UNI-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'PEPE-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'RENDER-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'TRUMP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
         },
    # "bitget_perp": {inst: {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None, "local_ts": None}
    #     for inst in INSTS},
    "bitget": {inst: {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None, "local_ts": None}
        for inst in INSTS},
}

async def main():
    await asyncio.gather(
        #okx(prices),
        okx_perp(prices),
        # kucoin_ws(prices),
        # buy_bit(prices),
        # gate_perp(prices),
        # mecx(prices),
        # kucoin_perp(prices),
        # gate(prices),
        #bitget_perp(prices),
        bitget(prices),
        writer_worker(),
        compare_loop()
    )

def is_fresh(book: dict, TTL_MS: int, now_ms) -> bool:
    if book["local_ts"] is None:
        return False
    return (now_ms - book["local_ts"]) <= TTL_MS


async def writer_worker(): # фуекция записи в эксель
    while True:
        row = await arbitrage_queue.get()

        try:
            await asyncio.to_thread(write_to_arbitrage, *row)
        except Exception as e:
            print(f"[WRITE ERROR] {e}")
        finally:
            arbitrage_queue.task_done()

def can_emit_signal(signal_key: str, cooldown_sec: float = 0) -> bool: # функция проверки сигнала
    now = time.time()
    last_ts = last_signal_time.get(signal_key, 0)

    if now - last_ts >= cooldown_sec:
        last_signal_time[signal_key] = now
        return True

    return False


async def compare_loop():
    USDT_AMOUNT = 20  # 20$
    MIN_SPREAD = 0.005  # 0.5% для старта
    TTL_MS = 500  # котировка считается свежей 0.5 сек
    last_dbg = 0
    common_pairs = (
        # set(prices["okx"].keys())
            set(prices["okx_perp"].keys())
            & set(prices["bitget"].keys())
    )
    while True:
        now_ms = int(time.time() * 1000)
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        for pair in common_pairs:
            okx_perp_book = prices["okx_perp"][pair]
            bitget_book = prices["bitget"][pair]

            if time.time() - last_dbg > 2:
                print(f"\nPAIR: {pair}")

                print("okx_perp:",
                      "ask=", okx_perp_book["ask"],
                      "bid=", okx_perp_book["bid"],
                      "local_ts=", okx_perp_book["local_ts"])

                # print("bitget_perp:",
                #       "ask=", bitget_perp_book["ask"],
                #       "bid=", bitget_perp_book["bid"],
                #       "local_ts=", bitget_perp_book["local_ts"])

                print("bitget_spot:",
                      "ask=", bitget_book["ask"],
                      "bid=", bitget_book["bid"],
                      "local_ts=", bitget_book["local_ts"])

                last_dbg = time.time()
            # есть ли все котировки
            if (#okx["ask"] is not None and okx["bid"] is not None
                    okx_perp_book["ask"] is not None and okx_perp_book["bid"] is not None
                    and bitget_book["ask"] is not None and bitget_book["bid"] is not None):

                # свежие ли данные

                # if ((now_ms - okx["ts"] <= TTL_MS) and (now_ms - okx_perp["ts"] <= TTL_MS) and (now_ms - kuc["ts"] <= TTL_MS) and  (now_ms - kuc_perp["ts"] <= TTL_MS)
                #         and (now_ms - buy_bit["ts"] <= TTL_MS) and (now_ms - gate_perp["ts"] <= TTL_MS) and (now_ms - mecx["ts"] <= TTL_MS) and (now_ms - gate["ts"] <= TTL_MS)
                #         and (now_ms - bitgate_perp["ts"] <= TTL_MS)):
                if (
                        is_fresh(okx_perp_book, TTL_MS, now_ms)
                        and is_fresh(bitget_book, TTL_MS, now_ms)
                ):

                    # Направление 1 PERP: BUY BITGET (ask) -> SELL OKX_perp (bid)'
                    buy = bitget_book["ask"]  # лучшая цена продажи
                    sell = okx_perp_book["bid"]  # лучшая цена покупки
                    need_base = USDT_AMOUNT / buy

                    if bitget_book["ask_qty"] >= need_base and okx_perp_book["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy  # спред, разница между биржами
                        if spread >= MIN_SPREAD:
                            signal_key = f"{pair}|BITGET->OKX_PERP"
                            if can_emit_signal(signal_key, cooldown_sec=0):
                            #write_to_arbitrage(buy, sell, spread, need_base, current_time, pair, 'Направление 1 PERP: BUY BITGET (ask) -> SELL OKX_perp (bid)')
                                try:
                                    arbitrage_queue.put_nowait([
                                        buy, sell, spread, need_base, current_time, pair,
                                        'Направление 1 PERP: BUY BITGET (ask) -> SELL OKX_perp (bid)'
                                    ])
                                except asyncio.QueueFull:
                                    pass

        await asyncio.sleep(0.05)  # 50 мс


if __name__ == '__main__':
    asyncio.run(main())
