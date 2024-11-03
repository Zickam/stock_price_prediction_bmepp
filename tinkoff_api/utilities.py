import asyncio
import os
from datetime import timedelta, datetime

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

async def getStockDataByTicker(ticker: str, from_datetime: datetime, interval: CandleInterval) -> list[HistoricCandle]:
    """returns list of tuples. Each tuple consists of: time, open_price at this time, close_price at this time"""

    data = []

    figi = await getFIGIByTicker(ticker)

    async with AsyncClient(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
        async for candle in client.get_all_candles(
                figi=figi,
                from_=from_datetime, # now() - timedelta(days=1)
                interval=interval
        ):
            # open_price = candle.open.units + candle.open.nano / 10 ** 9
            # close_price = candle.close.units + candle.close.nano / 10 ** 9
            # data.append((candle.time, open_price, close_price))
            data.append(candle)

    return data


async def getFIGIByTicker(ticker: str, class_code: str = "TQBR") -> str:
    return (await getAssetByTicker(ticker)).figi

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
    print(asyncio.run(getStockInfoByTicker("SBER")).eps)