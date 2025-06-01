import asyncio
from config import bot, dp, logger
from handlers.message_handlers import router

async def main():
    # Registra os handlers
    dp.include_router(router)
    
    try:
        logger.info("Bot iniciado")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Erro ao iniciar bot: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main()) 