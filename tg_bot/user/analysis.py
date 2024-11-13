from datetime import datetime
from datetime import timedelta

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import FSInputFile
from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import now

from analysis.functions import getSimplePriceChangeCoefficient, getSimplePriceChangeCoefficientByTicker
from tg_bot.user.localizations.get_localizations import getText
from tg_bot.user import keyboards
from tg_bot.user import filters
from tg_bot.user import states
from tg_bot.user.menu import showAnalysisMsg
import tinkoff_api
import plot
from tinkoff_api.utilities import getAssetByTicker, getStockDataByTicker, getStockInfoByTicker

analysis_router = Router()

days = 30 * 6
interval = CandleInterval.CANDLE_INTERVAL_DAY

async def handleChosenTicker(msg: Message, state: FSMContext, ticker: str):
    try:
        candles = await tinkoff_api.utilities.getStockDataByTicker(ticker, now() - timedelta(days=days), now(), interval)
        time_and_close = []
        for candle in candles:
            time_and_close.append((candle.time, candle.close.units + candle.close.nano / 10 ** 9))

    except Exception as ex:
        # raise ex
        text = (await getText("unexpected_ticker", state)).format(
            ticker=ticker
        )
        await msg.answer(text)
        await state.set_state(state=None)
        await showAnalysisMsg(msg, state)
        raise ex
        return

    plot.utilities.renderPlot(time_and_close, ticker)

    media = FSInputFile("tmp.png")

    price_change = await getSimplePriceChangeCoefficientByTicker(ticker, now() - timedelta(days=days), now(), interval)

    await msg.answer_photo(
        media,
        caption=f"*{ticker.upper()}* stock price changed by *{round(price_change * 100)}%*",
        parse_mode="Markdown"
    )

@analysis_router.message(StateFilter(states.Menu.choose_ticker))
async def handleAnalysisMsg(msg: Message, state: FSMContext):
    ticker = msg.text
    await handleChosenTicker(msg, state, ticker)

@analysis_router.callback_query(F.data.startswith("get_analysis_"))
async def handleAnalysisCall(call: CallbackQuery, state: FSMContext):
    ticker = call.data.replace("get_analysis_", "")
    await handleChosenTicker(call.message, state, ticker)

