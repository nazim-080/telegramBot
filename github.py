import telebot
import os
import shutil
from loguru import logger

from env import bot_token, teacher_git

bot = telebot.TeleBot(bot_token)

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


@logger.catch
def download_rep(git: str) -> int:
    git_student = git
    git_teacher = teacher_git
    global new_dir
    try:
        os.chdir('..')
        dir_now = os.getcwd()
        new_dir = os.path.join(dir_now, 'NewDirForProgram')
        os.mkdir(new_dir)
        logger.debug(f"Create new folder {os.getcwd()}")
    except FileExistsError:
        logger.debug(f"{FileExistsError}\nThe folder {new_dir} has already been created")
        os.system(f'rd /s /q "{new_dir}"')
        logger.debug(f"Delete folder {new_dir}")
        os.mkdir(new_dir)
        logger.debug(f"Create new folder {os.getcwd()}")
    os.chdir(new_dir)

    os.system(f'git clone {git_teacher}')
    os.system(f'git clone {git_student}')
    logger.debug(f"clone 2 rep:\n"
                 "{git_teacher}\n"
                 "{git_student}")

    new_dir_student = git_student[git_student.rfind('/') + 1:git_student.rfind('.git')]
    new_dir_teacher = git_teacher[git_teacher.rfind('/') + 1:git_teacher.rfind('.git')]
    source = os.path.join(new_dir, new_dir_student)
    dest = os.path.join(new_dir, new_dir_teacher)
    os.chdir(source)
    files = os.listdir(source)
    for f in files:
        if '.git' in f or f == 'README.md':
            continue
        shutil.move(os.path.join(source, f), dest)
    logger.debug("Moved all files except README.md and .git into one folder")

    os.chdir('..')
    os.chdir(dest)
    process_finished_with_exit_code = os.system('python -m unittest main_test.TestCalc.test_calc')
    logger.debug("Run unit tests")
    return process_finished_with_exit_code
