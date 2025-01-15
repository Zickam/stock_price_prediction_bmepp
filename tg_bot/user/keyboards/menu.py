import os

from aiogram.utils.keyboard import \
    ReplyKeyboardMarkup, \
    ReplyKeyboardBuilder, \
    KeyboardButton, \
    InlineKeyboardBuilder, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

# from db import models
from tg_bot.user.localizations.get_localizations import getText

async def askLanguage() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="РУС🇷🇺"))
    builder.add(KeyboardButton(text="ENG🇺🇸"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

async def showMenu(state: FSMContext) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Анализ"))
    builder.add(KeyboardButton(text="О нас"))
    # builder.add(KeyboardButton(text=await getText("keyboards.menu.language", state)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, is_persistent=True)

async def showAnalysisMenu(state: FSMContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    tickers = ["ydex", "sber", "sofl", "t"]

    for ticker in tickers:
        builder.add(
            InlineKeyboardButton(
                text=ticker.upper(),
                callback_data=f"get_analysis_{ticker}"
            )
        )

    builder.adjust(3)

    return builder.as_markup()