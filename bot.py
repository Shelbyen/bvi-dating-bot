import asyncio

from aiogram import Bot, Dispatcher

from src.config.project_config import settings
from src.handlers import user_registration, acne_assessment
from src.middlewares.permission_middleware import PermissionMiddleware


async def on_startup():
    print('Бот вышел в онлайн')


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()

    user_registration.router.message.middleware(PermissionMiddleware(False))
    acne_assessment.router.message.middleware(PermissionMiddleware())

    dp.include_routers(user_registration.router, acne_assessment.router)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
