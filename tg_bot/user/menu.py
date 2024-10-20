from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from tg_bot.user.localizations.get_localizations import getText, getTextByLang
from tg_bot.user import keyboards
from tg_bot.user import filters
from tg_bot.user import states

menu_router = Router()

tickers = ["sber", "yndx", "tcsg"]

async def start(msg, state):
    await msg.answer(
        await getText("welcome", state),
        reply_markup=await keyboards.menu.showMenu(state)
    )

@menu_router.message(Command("start"))
async def startMsg(msg: Message, state: FSMContext):
    if "language" not in await state.get_data():
        await msg.answer(
            text=await getTextByLang("choose_language", "en"),
            reply_markup=await keyboards.menu.askLanguage()
        )
        return

    await start(msg, state)

@menu_router.message(F.text == "ENG🇺🇸")
async def chooseEn(msg: Message, state: FSMContext):
    await state.update_data({"language": "en"})
    await start(msg, state)

@menu_router.message(F.text == "РУС🇷🇺")
async def chooseRu(msg: Message, state: FSMContext):
    await state.update_data({"language": "ru"})
    await start(msg, state)

@menu_router.message(filters.FilterKeyboardButton("keyboards.menu.about"))
async def showAboutMsg(msg: Message, state: FSMContext):
    await msg.answer(
        await getText("about", state)
    )

@menu_router.message(filters.FilterKeyboardButton("keyboards.menu.analysis"))
async def showAnalysisMsg(msg: Message, state: FSMContext):
    await msg.answer(
        await getText("choose_ticker", state),
        reply_markup=await keyboards.menu.showAnalysisMenu(state)
    )
    await state.set_state(states.Menu.choose_ticker)
