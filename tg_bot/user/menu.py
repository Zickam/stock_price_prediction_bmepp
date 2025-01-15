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

async def start(msg, state):
    await msg.answer(
        ("Привет! Это бот команды БМЕПП УрФУ, который является пользовательским интерфейсом"
        " для проекта по предсказанию вектора движения цен активов\n\n"
         "Бот предоставляет базовую информацию о тикере, а также с помощью модели "
         "анализирует новости с сайта investing.com, которые относятся к этому тикеру и на основе анализа этих "
         "новостей выдает общую оценку акции\n\n"
         "Движение цены вверх = акция перспективная\n"
         "Движение цены вниз = акция неперспективная\n"
         "Тикер это ID ценной бумаги на бирже\n"),
        reply_markup=await keyboards.menu.showMenu(state),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@menu_router.message(Command("start"))
async def startMsg(msg: Message, state: FSMContext):
    await state.update_data({"language": "ru"})

    await start(msg, state)

@menu_router.message(F.text == "ENG🇺🇸")
async def chooseEn(msg: Message, state: FSMContext):
    await state.update_data({"language": "en"})
    await start(msg, state)

@menu_router.message(F.text == "РУС🇷🇺")
async def chooseRu(msg: Message, state: FSMContext):
    await state.update_data({"language": "ru"})
    await start(msg, state)

@menu_router.message(F.text == "О нас")
async def showAboutMsg(msg: Message, state: FSMContext):
    await msg.answer(
        ("Главный разработчик: @nadpis_ne_imeet_smysla\n"
        "Тимлид: @deshp666\n"
        "Аналитик: @uzkate\n"
        "Разработчик: @n1nja147\n"
        "Разработчик: @Terafybo\n")
    )

@menu_router.message(F.text == "Анализ")
async def showAnalysisMsg(msg: Message, state: FSMContext):
    await msg.answer(
        ("Напишите тикер компании или выберите тикер кнопками внизу\n"
         "[Список всех доступных для анализа тикеров](https://github.com/Zickam/stock_price_prediction_bmepp/blob/main/tickers.txt)"),
        reply_markup=await keyboards.menu.showAnalysisMenu(state),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    await state.set_state(states.Menu.choose_ticker)
