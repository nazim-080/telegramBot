import telebot
from loguru import logger

from database import database_checking, database_insert, database_update
from github import download_rep

from env import bot_token

bot = telebot.TeleBot(bot_token)

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10  MB", compression="zip")


@logger.catch
def registration(message):
    lst = message.text.split(', ')
    if len(lst) != 5:
        logger.error("Неправильный формат сообщения")
        return bot.send_message(message.chat.id,
                                f'{message.from_user.first_name}, неправильный формат сообщения')

    nam = str(lst[0])
    nam = nam.split(' ')
    fam = nam[0]
    name = nam[1]
    patronymic = nam[2]
    group = lst[1]
    task = lst[2]
    variant = lst[3]
    git = lst[4]

    group_lst = ('212Б', '221Б', '214Б')
    if group not in group_lst:
        logger.error("Неправильно записана группа")
        return bot.send_message(message.chat.id,
                                f'{message.from_user.first_name}, неправильно записана группа')

    if int(task) < 1 or int(task) > 5:
        logger.error("Неправильный номер задания")
        return bot.send_message(message.chat.id,
                                f'{message.from_user.first_name}, неправильный номер задания'
                                f'\nВозможный номер задания от 1 до 5')

    if int(variant) < 1 or int(variant) > 5:
        logger.error("Неправильный номер варианта")
        return bot.send_message(message.chat.id,
                                f'{message.from_user.first_name}, неправильный номер варианта'
                                f'\nВозможный номер задания от 1 до 5')

    if 'github.com/' not in git:
        return bot.send_message(message.chat.id,
                                f'{message.from_user.first_name}, некоректная ссылка')

    logger.debug("Validation: ok")

    process_finished_with_exit_code = download_rep(git)
    if process_finished_with_exit_code == 0:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, Вы прошли проверку')
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, Вы не прошли проверку')

    if database_checking(fam, name, patronymic, group, task, variant) == 0:
        database_insert(fam, name, patronymic, group, task, variant, git, process_finished_with_exit_code)
        return bot.send_message(message.chat.id, f'{message.from_user.first_name}, Вы записаны в Базу Данных')
    else:
        database_update(fam, name, patronymic, group, task, variant, git, process_finished_with_exit_code)
        return bot.send_message(message.chat.id, f'{message.from_user.first_name}, Вы перезаписаны в Базу Данных')
