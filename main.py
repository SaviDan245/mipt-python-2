import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config_reader import config
from bot.handlers import add_link, base, send_offers, list_links, remove_link, send_realty_db, track, change_freq

logger = logging.getLogger(__name__)


# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode='MarkdownV2')
    dp = Dispatcher()

    dp.include_router(base.router)
    dp.include_router(add_link.router)
    dp.include_router(list_links.router)
    dp.include_router(remove_link.router)
    dp.include_router(send_offers.router)
    dp.include_router(send_realty_db.router)
    dp.include_router(track.router)
    dp.include_router(change_freq.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
