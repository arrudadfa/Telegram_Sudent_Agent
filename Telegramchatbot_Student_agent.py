import asyncio
from config import (
    bot, dp, logger, SYSTEM_PROMPT, 
    ALLOWED_GROUP_IDS, MAX_DAILY_RESPONSES, 
    LIMITED_GROUP_ID, TRIGGER_KEYWORDS
)
from handlers.message_handlers import router
from history import chat_history
from services.redacao_service import RedacaoService
from services.cronograma_service import CronogramaService
from aiogram import types
from datetime import datetime, timedelta

# Contador de respostas diárias
response_count = {LIMITED_GROUP_ID: 0}
reset_time = datetime.now() + timedelta(days=1)

# Função para resetar o contador diariamente
async def reset_daily_limit():
    global reset_time, response_count
    while True:
        if datetime.now() >= reset_time:
            response_count[LIMITED_GROUP_ID] = 0
            reset_time = datetime.now() + timedelta(days=1)
            logger.info("Contador de respostas diário resetado")
        await asyncio.sleep(3600)

# Handler para novos membros
@router.chat_member()
async def welcome_new_member(event: types.ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        new_member_name = event.new_chat_member.user.full_name
        welcome_message = f"Bem-vindo ao grupo, {new_member_name}!"
        await bot.send_message(event.chat.id, welcome_message)

# Handler principal de mensagens
@router.message()
async def message_handler(message: types.Message):
    logger.info(f"Recebido: {message.text}")
    await message.reply("Recebi sua mensagem!")

async def main():
    # Inicia a tarefa de reset diário
    asyncio.create_task(reset_daily_limit())
    
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