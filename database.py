import telebot
import psycopg2
from psycopg2 import Error

from env import *

bot = telebot.TeleBot(bot_token)

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


@logger.catch
def database_checking(fam, name, patronymic, grp, task, var) -> int:
    try:
        connection = psycopg2.connect(user=db_user,
                                      password=db_password,
                                      host=db_host,
                                      port=db_port,
                                      database=db_name)
        logger.debug("Connected to database")
        sql_checking = f"SELECT COUNT(name) FROM student WHERE fam = '{fam}' and name = '{name}' and " \
                       f"patronymic = '{patronymic}' and grp = '{grp}' and task = '{task}' and var = '{var}';"

        data = []
        cursor = connection.cursor()
        cursor.execute(sql_checking, data)
        results = cursor.fetchone()
        connection.commit()
        logger.debug(f"{results[0]} - same students")
    except (Exception, Error) as error:
        logger.exception(f"Error while working with PostgreSQL {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.debug("Database connection closed")

    return results[0]


@logger.catch
def database_update(fam, name, patronymic, grp, task, var, git, process_finished_with_exit_code) -> None:
    try:
        connection = psycopg2.connect(user=db_user,
                                      password=db_password,
                                      host=db_host,
                                      port=db_port,
                                      database=db_name)
        logger.debug("Connected to database")
        sql_update = f"UPDATE student set process = '{process_finished_with_exit_code}'" \
                     f"WHERE fam = '{fam}' and name = '{name}' and patronymic = '{patronymic}' and grp = '{grp}' and " \
                     f"task = '{task}' and var = '{var}' and git = '{git}';"

        cursor = connection.cursor()
        cursor.execute(sql_update)
        connection.commit()
        logger.debug("Student records are updated in the database")
    except (Exception, Error) as error:
        logger.exception(f"Error while working with PostgreSQL {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.debug("Database connection closed")


@logger.catch
def database_insert(fam, name, patronymic, grp, task, var, git, process_finished_with_exit_code) -> None:
    try:
        connection = psycopg2.connect(user=db_user,
                                      password=db_password,
                                      host=db_host,
                                      port=db_port,
                                      database=db_name)
        logger.debug("Connected to database")
        sql_insert = f"INSERT INTO student (fam,name,patronymic,grp,task,var,git,process) VALUES" \
                     f" ('{fam}','{name}', '{patronymic}', '{grp}', '{task}', '{var}', '{git}'," \
                     f" '{process_finished_with_exit_code}');"

        cursor = connection.cursor()
        cursor.execute(sql_insert)
        connection.commit()
        logger.debug("The student is registered in the database")
    except (Exception, Error) as error:
        logger.exception(f"Error while working with PostgreSQL {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.debug("Database connection closed")


@logger.catch
def print_res() -> str:
    try:
        connection = psycopg2.connect(user=db_user,
                                      password=db_password,
                                      host=db_host,
                                      port=db_port,
                                      database=db_name)

        logger.debug("Connected to database")
        cursor = connection.cursor()
        cursor.execute('SELECT fam, name, patronymic, grp, task, var, git, process FROM student')
        res = ''
        for row in cursor.fetchall():
            row = list(row)
            for j in range(len(row)):
                row[j] = str(row[j]).strip()
            res += ' | '.join(row) + '\n'
        logger.debug("Database output to telegram")
    except (Exception, Error) as error:
        logger.exception(f"Error while working with PostgreSQL {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.debug("Database connection closed")

    return res
