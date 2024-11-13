import datetime

from tinkoff.invest import CandleInterval

from tinkoff_api.utilities import getStockDataByTicker


def getSimplePriceChangeCoefficient(price_a, price_b) -> float:
    return (price_b - price_a) / price_a

async def getSimplePriceChangeCoefficientByTicker(
        ticker: str,
        datetime_a,
        datetime_b,
        intervals: CandleInterval
) -> float:
    candles = await getStockDataByTicker(ticker, datetime_a, datetime_b, intervals)
    return getSimplePriceChangeCoefficient(
        candles[0].open.units + candles[0].open.nano / 10 ** 9,
        candles[-1].close.units + candles[-1].close.nano / 10 ** 9
    )

def getSMAs(close_prices: list[float], window_size: int) -> list[float]:
    """simple moving average"""
    SMAs = []

    for i in range(window_size, len(close_prices) + 1):
        summ = 0
        for j in range(i - window_size, i):
            summ += close_prices[j]
        SMAs.append(summ / window_size)

    return SMAs

def getEMAs(close_prices: list[float], window_size: int, smoothing: float) -> list[float]:
    """exponential moving average"""
    EMAs = [close_prices[window_size] - 1] # maybe set as a first SMA, accordingly to https://tabtrader.com/ru/academy/articles/exponential-moving-average-ema-explained

    for i in range(window_size, len(close_prices)):
        tmp_smoothing = smoothing / (1 + window_size)
        EMA_today = close_prices[i] * tmp_smoothing + EMAs[-1] * (1 - tmp_smoothing)
        EMAs.append(EMA_today)

    return EMAs


if __name__ == "__main__":
    # from tinkoff_api.utilities import getStockDataByTicker
    # from tinkoff.invest.utils import now
    # from datetime import timedelta
    # import asyncio
    # data = asyncio.run(getStockDataByTicker("LKOH", now() - timedelta(days=30 * 6), CandleInterval.CANDLE_INTERVAL_DAY))
    # prices = []
    # for d in data:
    #     prices.append(d.close.units + d.close.nano / 10 ** 9)
    # print(getEMAs(prices, 30, 2))
    # import asyncio
    # stock_info = asyncio.run(getStockInfoByTicker("lkoh"))
    # print(stock_info)
    # calculateLynchFairValue(3312, stock_info)
    import asyncio
    print(asyncio.run(getSimplePriceChangeCoefficientByTicker(
        "LKOH",
        datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1),
        datetime.datetime.now(tz=datetime.timezone.utc),
        CandleInterval.CANDLE_INTERVAL_HOUR)
    ))
    # print(getSimplePriceChangeCoefficient(100, 50))
