# Это основной запускаемый файл.
# Заменить содержимое своим кодом.
from loader import bot
from commands import *

if __name__ == '__main__':
    bot.polling(none_stop=True)
