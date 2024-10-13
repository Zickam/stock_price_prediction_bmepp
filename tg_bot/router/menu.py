from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

menu_router = Router()