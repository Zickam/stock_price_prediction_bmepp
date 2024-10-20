import asyncio
import logging
import os

logging.basicConfig(level=logging.DEBUG)


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
import aiogram
from redis.asyncio import Redis

from tg_bot import user

redis = Redis(host="redis")

tg_bot_secret = os.getenv("TG_BOT_TOKEN")

bot = Bot(
        token=tg_bot_secret,
        default=DefaultBotProperties(
          parse_mode=aiogram.enums.ParseMode.HTML
        )
    )

bot.redis = redis

storage = RedisStorage(redis)

dp = Dispatcher(storage=storage)


async def main():

    # await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(
        user.router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())