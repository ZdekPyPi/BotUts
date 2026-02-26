from .loguru import *
from .api_monitor import *
from .task import *
from sys import argv


def terminal_opt():
    tasks = Task.TASKS
    task = list(tasks.keys())[0]
    logger_start(tasks[task]["function"])()
