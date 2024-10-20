import asyncio
import os
from datetime import timedelta

from tinkoff.invest import AsyncClient, CandleInterval, Client
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

async def getStockDataByTicker(ticker: str) -> ...:
    data = []

    figi = await getFIGIByTicker(ticker.upper())

    async with AsyncClient(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:

        async for candle in client.get_all_candles(
                figi=figi,
                from_=now() - timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_HOUR
        ):
            # raise Exception(candle.time, candle.close)
            data.append([candle.time, candle.close.units + candle.close.nano / 10 ** 9])

    return data


async def getFIGIByTicker(ticker: str, class_code: str = "TQBR"):
    with Client(TOKEN) as client:
        r = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, id=ticker, class_code=class_code)
        return r.instrument.figi

# asyncio.run(getStockData(FIGIS["sber"]))
# asyncio.run(findInstrumentByTicker("YDEX", "TQBR"))