from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from tg_bot.user.localizations.get_localizations import getText
from tg_bot.user import keyboards
from tg_bot.user import filters
from tg_bot.user import states
from tg_bot.user.menu import tickers
from tg_bot.user.menu import showAnalysisMsg

analysis_router = Router()

async def handleChosenTicker(msg: Message, state: FSMContext, ticker: str):
    if ticker not in tickers:
        text = (await getText("unexpected_ticker", state)).format(
            ticker=ticker
        )
        await msg.answer(text)
        await state.set_state(state=None)
        await showAnalysisMsg(msg, state)
        return

    await msg.answer(
        f"showing analysis for ticker {ticker}"
    )

@analysis_router.message(StateFilter(states.Menu.choose_ticker))
async def handleAnalysisMsg(msg: Message, state: FSMContext):
    ticker = msg.text
    await handleChosenTicker(msg, state, ticker)

@analysis_router.callback_query(F.data.startswith("get_analysis_"))
async def handleAnalysisCall(call: CallbackQuery, state: FSMContext):
    ticker = call.data.replace("get_analysis_", "")
    await handleChosenTicker(call.message, state, ticker)

