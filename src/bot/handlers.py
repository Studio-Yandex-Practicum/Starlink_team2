from loader import bot
# from request import start_chek_user
from telebot.types import Message
from utils.logger import get_logger

logger = get_logger(__name__)

@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    await bot.send_message(
        message.chat.id,
        'Приветственное сообщение для кандидатов'
    )
    logger.info(f'{message.from_user.username} запустил бота')
    # bd_user = await start_chek_user(message)
    # if bd_user.role == 0:
    #     bot.reply_to(message, 'Приветственное сообщение для кандидатов')
    # elif bd_user.role == 1:
    #     bot.reply_to(message, f'С возращением {bd_user.Name}!')
