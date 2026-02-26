from .api_monitor import *
from .task import *
from .bot_options import *
from .utils import *

import locale
from dateUts import now
from bot_lib.config import logger
from bot_lib.settings import botConfig


def show_config():
    def show_data(key, val): return logger.debug(f'{f"{key}:":<15}{val}')
    # ===================== MOSTRA AS CONFIGURACOES ATUAIS DO BOT
    logger.debug((f'===================== CONFIG ================'))
    show_data("BOT_NAME", botConfig.BOT_NAME)
    show_data("TIME", f'{now(fmt="sql+hr")} {locale.getlocale()[0]}')
    show_data("LOCALE", locale.getlocale()[0])
    show_data("MODE", os.getenv("MODE", "DEV"))
    logger.debug(f'===================== TASKS')
    size = max([len(task) + 1 for task in Task.TASKS] or [0])
    for task in Task.TASKS:
        cron = Task.TASKS[task]["cron"]
        logger.debug(f"{(task + ':').ljust(size)} {cron}")
    logger.debug(f'===================== CONFIG ================')
