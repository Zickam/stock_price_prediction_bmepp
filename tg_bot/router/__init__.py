from aiogram import Router

from menu import menu_router

router = Router()

router.include_routers(
    menu_router
)