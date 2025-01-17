import logging
import asyncio
import os
from datetime import timedelta, datetime
# from main import logging

from tinkoff.invest import AsyncClient, CandleInterval, Client, Candle, HistoricCandle, GetAssetFundamentalsResponse, \
    GetAssetFundamentalsRequest, InstrumentResponse, Instrument, StatisticResponse
from tinkoff.invest.utils import now
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from tinkoff.invest.async_services import AsyncServices, InstrumentIdType


TOKEN = os.getenv("TINKOFF_INVESTMENTS_TOKEN")

client = AsyncClient(TOKEN)

async def getStockDataByFIGI(figi: str) -> ...:
    data = []

    async with AsyncClient(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        async for candle in client.get_all_candles(
                figi=figi,
                from_=now() - timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_HOUR
        ):
            data.append([candle.time, candle.close])

    return data


async def getStockDataByTicker(
        ticker: str,
        from_datetime: datetime,
        to_datetime: datetime,
        interval: CandleInterval
) -> list[HistoricCandle]:
    """for ranges"""
    data = []

    figi = await getFIGIByTicker(ticker)

    async with AsyncClient(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        async for candle in client.get_all_candles(
                figi=figi,
                from_=from_datetime,  # now() - timedelta(days=1)
                to=to_datetime,
                interval=interval
        ):
            data.append(candle)

    return data


intervals = [
    CandleInterval.CANDLE_INTERVAL_HOUR,
    CandleInterval.CANDLE_INTERVAL_1_MIN,
    CandleInterval.CANDLE_INTERVAL_2_MIN,
    CandleInterval.CANDLE_INTERVAL_3_MIN,
    CandleInterval.CANDLE_INTERVAL_5_MIN,
    CandleInterval.CANDLE_INTERVAL_10_MIN,
    CandleInterval.CANDLE_INTERVAL_15_MIN,
    CandleInterval.CANDLE_INTERVAL_30_MIN,
]

async def getStockCostByTicker(ticker: str, _datetime: datetime = None) -> float:
    if _datetime is None:
        _datetime = now()

    figi = await getFIGIByTicker(ticker)
    last_cost = None

    async with AsyncClient(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        for interval in intervals:
            logging.info(f"interval {interval}")
            async for candle in client.get_all_candles(
                figi=figi,
                to=_datetime - timedelta(minutes=2),
                from_=_datetime - timedelta(days=7),
                interval=interval
            ):
                last_cost = candle.close.units + candle.close.nano / 10 ** 9
            if last_cost is not None:
                break

    return last_cost

async def getFIGIByTicker(ticker: str, class_code: str = "TQBR") -> str:
    return (await getAssetByTicker(ticker, class_code)).figi

async def getAssetByTicker(ticker: str, class_code: str = "TQBR") -> Instrument:
    with Client(TOKEN) as client:
        r = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, id=ticker.upper(), class_code=class_code)
        return r.instrument


async def getStockInfoByTicker(ticker: str) -> StatisticResponse:
    asset = await getAssetByTicker(ticker)

    with Client(TOKEN) as client:
        request = GetAssetFundamentalsRequest(assets=[asset.asset_uid])
        r = client.instruments.get_asset_fundamentals(request)
        return r.fundamentals[0]


if __name__ == "__main__":
    # print(asyncio.run(getStockInfoByTicker("SBER")))
    # print(asyncio.run(getStockCostByTicker("VKCO", now())))
    ...