import asyncio, time
from okx import okx
from ku_koin import kucoin_ws
from buy_bit import buy_bit
from mexc_perp import mecx_perp
from exel import write_to_arbitrage
from okx_perp import okx_perp
from mecx import mecx

# Спот
prices = {
    "okx": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
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
    "okx_perp": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
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
            #'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
            'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
            },
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
    "mecx_perp": {'TON-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
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
             # 'FIL-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'FLR-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'JUP-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
             'PENGU-USDT': {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None}
             }
}

async def main():
    await asyncio.gather(
        okx(prices),
        okx_perp(prices),
        kucoin_ws(prices),
        buy_bit(prices),
        mecx_perp(prices),
        mecx(prices),
        compare_loop()
    )


async def compare_loop():
    USDT_AMOUNT = 10  # 10$
    MIN_SPREAD = 0.006  # 0.6% для старта
    TTL_MS = 10000  # котировка считается свежей 10 сек
    last_dbg = 0
    while True:
        common_pairs = (
                set(prices["okx"].keys())
                & set(prices["okx_perp"].keys())
                & set(prices["kucoin"].keys())
                & set(prices["buy_bit"].keys())
                & set(prices["mecx_perp"].keys())
                & set(prices["mecx"].keys())
        )

        for pair in common_pairs:
            #print(pair)
            okx = prices["okx"][pair]
            okx_perp = prices["okx_perp"][pair]
            kuc = prices["kucoin"][pair]
            buy_bit = prices["buy_bit"][pair]
            mecx_perp = prices["mecx_perp"][pair]
            mecx = prices["mecx"][pair]
            if time.time() - last_dbg > 2:
                print(f'okx {okx}')
                print(f'okx_perp {okx_perp}')
                print(f'kuc {kuc}')
                print(f'buy_bit {buy_bit}')
                print(f'mecx_perp {mecx_perp}')
                print(f'mecx {mecx}')
                last_dbg = time.time()
            # есть ли все котировки
            if (okx["ask"] is not None and okx["bid"] is not None
                    and okx_perp["ask"] is not None and okx_perp["bid"] is not None
                    and kuc["ask"] is not None and kuc["bid"] is not None
                    and buy_bit["ask"] is not None  and buy_bit["bid"] is not None
                    and mecx["ask"] is not None and mecx["bid"] is not None
                    and mecx_perp["ask"] is not None and mecx_perp["bid"] is not None):

                now_ms = int(time.time() * 1000)
                current_time = time.strftime("%H:%M:%S")

                # свежие ли данные

                if ((now_ms - okx["ts"] <= TTL_MS) and (now_ms - okx_perp["ts"] <= TTL_MS) and (now_ms - kuc["ts"] <= TTL_MS)
                        and (now_ms - buy_bit["ts"] <= TTL_MS) and (now_ms - mecx_perp["ts"] <= TTL_MS) and (now_ms - mecx["ts"] <= TTL_MS)):

                    # Направление 1: BUY OKX (ask) -> SELL KuCoin (bid)
                    buy = okx["ask"]  # лучшая цена продажи
                    sell = kuc["bid"]  # лучшая цена покупки
                    need_base = USDT_AMOUNT / buy

                    if okx["ask_qty"] >= need_base and kuc["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy  # пред, разница между биржами
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair, 'Направление 1: BUY OKX (ask) -> SELL KuCoin (bid)')

                    # Направление 2: BUY KuCoin (ask) -> SELL OKX_perp (bid)
                    buy = kuc["ask"]
                    sell = okx_perp["bid"]
                    need_base = USDT_AMOUNT / buy

                    if kuc["ask_qty"] >= need_base and okx_perp["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair, 'Направление 2: BUY KuCoin (ask) -> SELL OKX_perp (bid)')

                    # Направление 3: BUY Buy_bit (ask) -> SELL KuCoin (bid)
                    buy = buy_bit["ask"]  # лучшая цена продажи
                    sell = kuc["bid"]  # лучшая цена покупки
                    need_base = USDT_AMOUNT / buy

                    if buy_bit["ask_qty"] >= need_base and kuc["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy  # пред, разница между биржами
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair, 'Направление 3: BUY Buy_bit (ask) -> SELL KuCoin (bid)')

                    # Направление 4: BUY KuCoin (ask) -> SELL Buy_bit (bid)
                    buy = kuc["ask"]
                    sell = buy_bit["bid"]
                    need_base = USDT_AMOUNT / buy

                    if kuc["ask_qty"] >= need_base and buy_bit["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy
                        if spread >= MIN_SPREAD:
                            #print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair, 'Направление 4: BUY KuCoin (ask) -> SELL Buy_bit (bid)')

                    # Направление 5: BUY OKX (ask) -> SELL mecx_perp (bid)
                    buy = okx["ask"]  # лучшая цена продажи
                    sell = mecx_perp["bid"]  # лучшая цена покупки
                    need_base = USDT_AMOUNT / buy

                    if okx["ask_qty"] >= need_base and mecx_perp["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy  # пред, разница между биржами
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair,'Направление 5: BUY OKX (ask) -> SELL mecx_perp (bid)')

                    # Направление 6: BUY mecx (ask) -> SELL OKX_perp (bid)
                    buy = mecx["ask"]
                    sell = okx_perp["bid"]
                    need_base = USDT_AMOUNT / buy

                    if mecx["ask_qty"] >= need_base and okx_perp["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair,'Направление 6: BUY mecx (ask) -> SELL OKX_perp (bid)')

                    # Направление 7: BUY Buy_bit (ask) -> SELL mecx_perp (bid)
                    buy = buy_bit["ask"]  # лучшая цена продажи
                    sell = mecx_perp["bid"]  # лучшая цена покупки
                    need_base = USDT_AMOUNT / buy

                    if buy_bit["ask_qty"] >= need_base and mecx_perp["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy  # пред, разница между биржами
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair,'Направление 7: BUY Buy_bit (ask) -> SELL mecx_perp (bid)')

                    # Направление 8: BUY mecx (ask) -> SELL Buy_bit (bid)
                    buy = mecx["ask"]
                    sell = buy_bit["bid"]
                    need_base = USDT_AMOUNT / buy

                    if mecx["ask_qty"] >= need_base and buy_bit["bid_qty"] >= need_base:
                        spread = (sell - buy) / buy
                        if spread >= MIN_SPREAD:
                            # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                            write_to_arbitrage(buy, sell, spread, need_base, current_time, pair,'Направление 8: BUY mecx (ask) -> SELL Buy_bit (bid)')

        await asyncio.sleep(0.2)  # 200 мс


if __name__ == '__main__':
    asyncio.run(main())
