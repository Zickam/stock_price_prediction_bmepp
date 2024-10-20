from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tg_bot.user.localizations.get_localizations import getText

class FilterKeyboardButton(BaseFilter):
    def __init__(self, locale_path: str):
        self.locale_path = locale_path

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if await getText(self.locale_path, state) == message.text:
            return True
        return False
