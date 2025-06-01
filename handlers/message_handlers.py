from aiogram import types
from config import router, logger
from services.redacao_service import RedacaoService
from services.cronograma_service import CronogramaService
from history import chat_history

@router.message()
async def handle_message(message: types.Message):
    if not message.text:
        return
    
    # Adiciona mensagem ao histórico
    chat_history.add_message(message.from_user.id, message.text)
    
    texto = message.text.lower()
    logger.info(f"Mensagem recebida de {message.from_user.id}: {texto}")

    # Processamento baseado no comando
    if texto.startswith('/redacao'):
        notas, feedback = await RedacaoService.corrigir_redacao(texto)
        await message.reply(feedback)
        
    elif texto.startswith('/cronograma'):
        # Processar comando de cronograma
        pass 