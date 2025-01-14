import logging
import math
import datetime

from tinkoff.invest import CandleInterval

from tinkoff_api.utilities import getStockDataByTicker, getStockCostByTicker

def getSimplePriceChange(price_a: float, price_b: float) -> float:
    try:
        return (price_b - price_a) / price_a
    except ZeroDivisionError:
        return 0
    except TypeError:
        return 0

def getTanHNormalizedPriceChange(price_a: float, price_b: float) -> float:
    return math.tanh(getSimplePriceChange(price_a, price_b))

async def getTanHNormalizedPriceChangeByTicker(
        ticker: str,
        datetime_a: datetime.datetime,
        datetime_b: datetime.datetime
) -> float:
    cost_a = await getStockCostByTicker(ticker, datetime_a)
    cost_b = await getStockCostByTicker(ticker, datetime_b)
    return getTanHNormalizedPriceChange(
        cost_a,
        cost_b
    )

async def getSimplePriceChangeByTicker(
        ticker: str,
        datetime_a: datetime.datetime,
        datetime_b: datetime.datetime
) -> float:
    cost_a = await getStockCostByTicker(ticker, datetime_a)
    cost_b = await getStockCostByTicker(ticker, datetime_b)
    return getSimplePriceChange(
        cost_a,
        cost_b
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
    import asyncio
    # data = asyncio.run(getStockDataByTicker("LKOH", now() - timedelta(days=30 * 6), CandleInterval.CANDLE_INTERVAL_DAY))
    # prices = []
    # for d in data:
    #     prices.append(d.close.units + d.close.nano / 10 ** 9)
    # print(getEMAs(prices, 30, 2))
    # import asyncio
    # stock_info = asyncio.run(getStockInfoByTicker("lkoh"))
    # print(stock_info)
    # calculateLynchFairValue(3312, stock_info)
    # import asyncio
    # print(asyncio.run(getSimplePriceChangeCoefficientByTicker(
    #     "LKOH",
    #     datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=180),
    #     datetime.datetime.now(tz=datetime.timezone.utc),
    #     CandleInterval.CANDLE_INTERVAL_DAY)
    # ))
    # print(getSimplePriceChangeCoefficient(100, 50))
    a, b = 30, 40
    print(getSimplePriceChangeCoefficient(a, b))
    print(getSimplePriceChangeCoefficient(b, a))