import os
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

from tg_bot.user.localizations.get_localizations import getText
from tg_bot.user import keyboards
from tg_bot.user import filters
from tg_bot.user import states
from tg_bot.user.menu import showAnalysisMsg
import tinkoff_api
import plot
from tinkoff_api.utilities import getAssetByTicker, getStockDataByTicker, getStockInfoByTicker
from tg_bot.report_maker import ReportMaker
from aiogram.utils.media_group import MediaGroupBuilder



analysis_router = Router()

days = 30 * 6
interval = CandleInterval.CANDLE_INTERVAL_DAY

async def handleChosenTicker(msg: Message, state: FSMContext, ticker: str):
    report = await ReportMaker.makeReport(state, ticker)
    if not report.status:
        await msg.answer(report.status_description, parse_mode="HTML")
        await state.set_state(state=None)
        await showAnalysisMsg(msg, state)
        return

    media_group = MediaGroupBuilder(caption=report.text)

    for photo in report.photos:
        media = FSInputFile(photo)
        media_group.add_photo(type="photo", media=media, parse_mode="Markdown")

    await msg.answer_media_group(media=media_group.build())

    await report.clear()


@analysis_router.message(StateFilter(states.Menu.choose_ticker))
async def handleAnalysisMsg(msg: Message, state: FSMContext):
    ticker = msg.text
    await handleChosenTicker(msg, state, ticker)

@analysis_router.callback_query(F.data.startswith("get_analysis_"))
async def handleAnalysisCall(call: CallbackQuery, state: FSMContext):
    ticker = call.data.replace("get_analysis_", "")
    await handleChosenTicker(call.message, state, ticker)

