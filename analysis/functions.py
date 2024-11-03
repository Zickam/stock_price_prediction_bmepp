from tinkoff.invest import CandleInterval


def getSimplePriceChangeCoefficient(price_a, price_b) -> float:
    return 1 + (price_b - price_a) / price_a

def getSMAs(close_prices: list[float], window_size: int) -> list[float]:
    """simple moving average"""
    SMAs = []

    for i in range(window_size, len(close_prices) + 1):
        summ = 0
        for j in range(i - window_size, i):
            summ += close_prices[j]
        SMAs.append(summ / window_size)

    return SMAs

def getEMA():
    """exponential moving average"""



if __name__ == "__main__":
    from tinkoff_api.utilities import getStockDataByTicker
    from tinkoff.invest.utils import now
    from datetime import timedelta
    import asyncio
    data = asyncio.run(getStockDataByTicker("LKOH", now() - timedelta(days=30 * 6), CandleInterval.CANDLE_INTERVAL_DAY))
    prices = []
    for d in data:
        prices.append(d.close.units + d.close.nano / 10 ** 9)
    print(getSMAs(prices, 30))
