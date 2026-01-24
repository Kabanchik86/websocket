import asyncio, time
from okx import okx
from ku_koin import kucoin_ws
from exel import write_to_arbitrage

prices = {
    "okx": {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
    "kucoin": {"ask": None, "bid": None, "ask_qty": None, "bid_qty": None, "ts": None},
}


async def main():
    await asyncio.gather(
        okx(prices),
        kucoin_ws(prices),
        compare_loop()
    )


async def compare_loop():
    USDT_AMOUNT = 10  # 10$
    MIN_SPREAD = 0.005  # 0.5% для старта
    TTL_MS = 6000  # котировка считается свежей 8 сек

    while True:
        okx = prices["okx"]
        kuc = prices["kucoin"]

        # есть ли обе котировки
        if okx["ask"] and okx["bid"] and kuc["ask"] and kuc["bid"]:
            now_ms = int(time.time() * 1000)
            current_time = time.strftime("%H:%M:%S")
            # print(okx['ts'])
            # print(now_ms - okx["ts"])
            # print(TTL_MS)
            # свежие ли данные
            if (now_ms - okx["ts"] <= TTL_MS) and (now_ms - kuc["ts"] <= TTL_MS):

                # Направление 1: BUY OKX (ask) -> SELL KuCoin (bid)
                buy = okx["ask"]  # лучшая цена продажи
                sell = kuc["bid"]  # лучшая цена покупки
                need_base = USDT_AMOUNT / buy

                if okx["ask_qty"] >= need_base and kuc["bid_qty"] >= need_base:
                    spread = (sell - buy) / buy  # пред, разница между биржами
                    if spread <= MIN_SPREAD:
                        # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                        write_to_arbitrage(buy, sell, spread, need_base, current_time)

                # Направление 2: BUY KuCoin (ask) -> SELL OKX (bid)
                buy = kuc["ask"]
                sell = okx["bid"]
                need_base = USDT_AMOUNT / buy

                if kuc["ask_qty"] >= need_base and okx["bid_qty"] >= need_base:
                    spread = (sell - buy) / buy
                    if spread >= MIN_SPREAD:
                        # print(f"[ARB] BUY OKX @{buy} -> SELL KUCOIN @{sell} | {spread*100:.2f}% | need {need_base:.4f} TON")
                        write_to_arbitrage(buy, sell, spread, need_base, current_time)

        await asyncio.sleep(0.2)  # 200 мс


if __name__ == '__main__':
    asyncio.run(main())
