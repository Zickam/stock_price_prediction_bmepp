import pickle
import math
import datetime
import os
import time

from grpc.beta.interfaces import StatusCode
from tinkoff.invest import Instrument, InstrumentIdType, CandleInterval
from tinkoff.invest.clients import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from tinkoff.invest.utils import now
import tinkoff

TOKEN = os.getenv("TINKOFF_INVESTMENTS_TOKEN")

client = Client(TOKEN)



def getSimplePriceChange(price_a: float, price_b: float) -> float:
    return (price_b - price_a) / price_a

def getTanHNormalizedPriceChange(price_a: float, price_b: float) -> float:
    return math.tanh(getSimplePriceChange(price_a, price_b))

def getTanHNormalizedPriceChangeByTicker(
        ticker: str,
        datetime_a: datetime.datetime,
        datetime_b: datetime.datetime
) -> float:
    cost_a = getStockCostByTicker(ticker, datetime_a)
    cost_b = getStockCostByTicker(ticker, datetime_b)
    if cost_a is None or cost_b is None:
        return None
    return getTanHNormalizedPriceChange(
        cost_a,
        cost_b
    )

intervals = {
    CandleInterval.CANDLE_INTERVAL_1_MIN: 1,
    CandleInterval.CANDLE_INTERVAL_2_MIN: 2,
    CandleInterval.CANDLE_INTERVAL_3_MIN: 3,
    CandleInterval.CANDLE_INTERVAL_5_MIN: 5,
    CandleInterval.CANDLE_INTERVAL_10_MIN: 10,
    CandleInterval.CANDLE_INTERVAL_15_MIN: 15,
    CandleInterval.CANDLE_INTERVAL_30_MIN: 30,
    CandleInterval.CANDLE_INTERVAL_HOUR: 60,
    CandleInterval.CANDLE_INTERVAL_2_HOUR: 60 * 2,
    CandleInterval.CANDLE_INTERVAL_4_HOUR: 60 * 4,
    CandleInterval.CANDLE_INTERVAL_DAY: 60 * 24,
    CandleInterval.CANDLE_INTERVAL_WEEK: 60 * 24 * 7,
    CandleInterval.CANDLE_INTERVAL_MONTH: 60 * 24 * 30
}

def getStockCostByTicker(ticker: str, _datetime: datetime = None) -> float:
    if _datetime is None:
        _datetime = now()

    figi = getFIGIByTicker(ticker)
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        for interval_enum, interval_minutes in intervals.items():
            # print(ticker, _datetime, interval_enum, interval_minutes)
            for candle in client.get_all_candles(
                    figi=figi,
                    from_=_datetime - datetime.timedelta(minutes=interval_minutes), # due to delay of stock data fetching through tinkoff api
                    # to=_datetime - timedelta(minutes=1), # due to delay of stock data fetching through tinkoff api
                    interval=interval_enum
            ):
                # print(candle)
                return candle.close.units + candle.close.nano / 10 ** 9

    print("Not found cost for", ticker, _datetime)

def getAssetByTicker(ticker: str, class_code: str = "TQBR") -> Instrument:
    path = "../analysis/instruments"
    if ticker not in os.listdir(path):
        r = None
        with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
            try:
                r = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, id=ticker.upper(), class_code=class_code)
            except tinkoff.invest.exceptions.RequestError as ex:
                while r is None:
                    if ex.code == StatusCode.RESOURCE_EXHAUSTED:
                        time.sleep(60)
                    r = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
                                                             id=ticker.upper(), class_code=class_code)
        with open(f"{path}/{ticker}", "wb") as file:
            pickle.dump(r.instrument, file)
        intrument = r.instrument

    else:
        with open(f"{path}/{ticker}", "rb") as file:
            intrument = pickle.load(file)

    return intrument


def getFIGIByTicker(ticker: str, class_code: str = "TQBR") -> str:
    return getAssetByTicker(ticker, class_code).figi


if __name__ == "__main__":
    print(getStockCostByTicker("sber"))