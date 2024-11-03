from datetime import datetime

import matplotlib.pyplot as plt


def renderPlot(data_close_prices: list[tuple[datetime, float]], ticker: str):
    plt.figure(figsize=(7, 7))
    plt.tick_params(axis='x', rotation=60)

    t = []
    s = []

    for i in range(len(data_close_prices)):
        t.append(data_close_prices[i][0])
        s.append(data_close_prices[i][1])

    for i in range(len(t) - 1):
        x_segment = t[i:i + 2]
        y_segment = s[i:i + 2]
        if s[i] < s[i + 1]:
            color = "g"
        elif s[i] > s[i + 1]:
            color = "r"
        else:
            color = "gray"
        plt.plot(x_segment, y_segment, color=color) #

    plt.xlabel('time(Hour)')
    plt.ylabel("price(RUB)")
    plt.title(ticker.upper())
    plt.grid()

    plt.savefig("tmp.png")

if __name__ == "__main__":
    import asyncio

    from tinkoff.invest.utils import now
    from datetime import timedelta
    import tinkoff_api
    from tinkoff.invest import CandleInterval

    ticker = "LKOH"

    time_and_open_and_close = asyncio.run(tinkoff_api.utilities.getStockDataByTicker(ticker, now() - timedelta(days=1),
                                                                               CandleInterval.CANDLE_INTERVAL_5_MIN))
    time_and_close = []
    for triple in time_and_open_and_close:
        time_and_close.append((triple[0], triple[1]))
    renderPlot(time_and_close, ticker)