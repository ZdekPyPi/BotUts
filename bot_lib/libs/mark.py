from bot_lib.database.orm import Log
from bot_lib import botConfig
from bot_lib import logger

TO_COMMIT = []


def mark_inter(seconds: int, description: str = "", commit=True):
    if botConfig.is_in_prd and botConfig.LOG_DB:
        if commit:
            logger.inter(description, extra_1=str(seconds), depth=2)
        else:
            TO_COMMIT.append((seconds, description))


def commit_mark_inter():
    for seconds, description in TO_COMMIT:
        logger.info(f"Commitando {len(TO_COMMIT)} marcações de INTER", depth=2)
    TO_COMMIT.clear()


def mark_job(type_job: str, description: str = "", qtd: int = 1):
    if botConfig.is_in_prd and botConfig.LOG_DB:
        logger.job(f"{type_job} | {description}", extra_1=str(qtd), depth=2)
