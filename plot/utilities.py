from datetime import datetime

import matplotlib.pyplot as plt

from analysis.functions import getSMAs, getEMAs


def renderPlot(data_close_prices: list[tuple[datetime, float]], ticker: str):
    plt.figure(figsize=(7, 7))
    plt.tick_params(axis='x', rotation=60)

    datetimes = []
    close_prices = []

    for i in range(len(data_close_prices)):
        datetimes.append(data_close_prices[i][0])
        close_prices.append(data_close_prices[i][1])

    window_size = 8
    SMAs = getSMAs(close_prices, window_size)
    EMAs = getEMAs(close_prices, window_size, 2)

    for i in range(len(datetimes) - 1):
        x_segment = datetimes[i:i + 2]
        y_segment = close_prices[i:i + 2]
        if close_prices[i] < close_prices[i + 1]:
            color = "g"
        elif close_prices[i] > close_prices[i + 1]:
            color = "r"
        else:
            color = "gray"
        plt.plot(x_segment, y_segment, color=color)

    smas_datetimes = datetimes[window_size - 1:len(datetimes)]
    plt.plot(smas_datetimes, SMAs, "-.", label="SMA", linewidth=1, alpha=0.8)

    emas_datetimes = datetimes[window_size - 1:len(datetimes)]
    plt.plot(emas_datetimes, EMAs, "--", label="EMA", linewidth=1, alpha=0.8)

    plt.xlabel('datetime')
    plt.ylabel("price(RUB)")
    plt.title(ticker.upper())
    plt.grid()
    plt.legend()

    plt.savefig("tmp.png")

if __name__ == "__main__":
    import asyncio

    from tinkoff.invest.utils import now
    from datetime import timedelta
    import tinkoff_api
    from tinkoff.invest import CandleInterval

    ticker = "LKOH"

    time_and_open_and_close = asyncio.run(tinkoff_api.utilities.getStockDataByTicker(ticker, now() - timedelta(days=30 * 6),
                                                                               CandleInterval.CANDLE_INTERVAL_DAY))
    time_and_close = []
    for candle in time_and_open_and_close:
        time_and_close.append((candle.time, candle.close.units + candle.close.nano / 10 ** 9))
    renderPlot(time_and_close, ticker)