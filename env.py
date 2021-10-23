import sys
import os
import yaml
from loguru import logger

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


@logger.catch
def check_env(envs: list) -> list:
    """
    Loads variables from ENV. If it does not find them in ENV,
    it tries to find them in file config.yaml. If I didn't find it there,
    it returns an error (exit code 1).
    """

    normal_env = []
    bad_env = []
    for env in envs:
        if os.getenv(env) is not None:
            normal_env.append(os.getenv(env))
            logger.debug(f"ENV {env} has been set")
        else:
            logger.debug(
                f"Env '{env}' doesn't set. Try to load it from config.yaml")
            try:
                with open(r"config.yaml") as file:
                    config = yaml.load(file, Loader=yaml.FullLoader)
                    if config[env]:
                        normal_env.append(config[env])
                        logger.debug("\tsuccess")
                    else:
                        bad_env.append(env)
            except FileNotFoundError:
                logger.error(
                    "We don't find a file config.yaml. Set variables in env or config.yaml")
                sys.exit(1)
            except KeyError:
                bad_env.append(env)
    if bad_env:
        logger.error("We can't find these names in ENV or config.yaml:")
        for i in bad_env:
            logger.error(f"\t{i}")
        logger.error("Please set all the necessary variables")
        sys.exit(1)
    return normal_env


[bot_token, db_name, db_user, db_password, db_host, db_port, teacher_git] = check_env(["BOT_TOKEN", "DB_NAME",
                                                                                       "DB_USER", "DB_PASSWORD",
                                                                                       "DB_HOST", "DB_PORT",
                                                                                       "TEACHER_GIT"])
