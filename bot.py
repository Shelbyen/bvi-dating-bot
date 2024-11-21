import asyncio

from aiogram import Bot, Dispatcher

from config.project_config import settings
from handlers import user


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    # dp.callback_query.outer_middleware(LogMiddleware())
    # dp.message.outer_middleware(LogMiddleware())
    # admin.router.message.middleware(PermissionMiddleware())
    #
    dp.include_routers(user.router)
    #
    # dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
