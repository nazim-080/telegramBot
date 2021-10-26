import telebot
from loguru import logger

from functions_student import registration
from database import print_res

from env import bot_token

bot = telebot.TeleBot(bot_token)

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, пришли мне ФИО, номер группы,\n'
                                      f'номер задания, номер варианта и ссылку на гитхаб в таком виде:\n'
                                      f'Иванов Иван Иванович, 312Б, 3, 4, git_ref')
    logger.debug("Bot sent a message to the command /start")


@bot.message_handler(commands=['database'])
def database(message):
    bot.send_message(message.chat.id, print_res())
    logger.debug("database(message) function worked")


@bot.message_handler(content_types=['text'])
def student_register(message):
    registration(message)
    logger.debug("student_register(message) function worked")


if __name__ == '__main__':
    bot.polling(none_stop=True)
