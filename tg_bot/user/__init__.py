from mailbox import Message

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tg_bot.user.menu import menu_router
from tg_bot.user.analysis import analysis_router

router = Router()

debug_router = Router()

router.include_routers(
    menu_router,
    analysis_router,
    debug_router
)

@debug_router.callback_query()
async def debugCall(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"[DEBUG] Unexpected callback: {call.data}")

@debug_router.message()
async def debugMsg(msg: Message, state: FSMContext):
    await msg.answer(f"[DEBUG] Unexpected message text: {msg.text}")