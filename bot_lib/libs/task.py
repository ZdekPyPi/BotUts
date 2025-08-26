from functools import wraps
from time import sleep
import pycron
import os
import bot_lib
from bot_lib.logger import logger
from bot_lib.database.orm import Log,BotInfo
from bot_lib.settings import botConfig


class Task:
    TASKS = {}

    def schedulled_tasks():
        return {k:v for k,v in Task.TASKS.items() if not v["local"]}

    def config(task_name, cron=None,local=False,comment=None):
        def decorator(function):

            if len(task_name) >15:
                raise Exception(f"Nome da task deve ter no maximo 15 caracteres!")
            
            if task_name in Task.TASKS:
                raise Exception(f"Task ({task_name}) já utilizada!")
            
            #VALDADE CRON QUERIES
            if not local:
                if not cron:
                    raise Exception("Please inform a CRON query!")
                if len(cron.split(" ")) != 5:
                    raise Exception(f"Invalid CRON! ({cron})")
            
        
            Task.TASKS[task_name] = {"function_name":function.__name__,"function":function,"local":local,"cron":cron,"comment":comment}
            function.__TASKNAME__ = task_name

            if bot_lib.IN_PRD and not local:
                crn = Log(level="CRON",message=cron)
                crn.task_name = task_name
                crn.save()

            @wraps(function)
            def wrapper(*args, **kwargs):
                logger.info(f"========== TASK({task_name}) ===========")
                function(*args, **kwargs)
            return wrapper
        return decorator
    
    def loop():
        from .loguru import logger_start
        schedulled_tasks = Task.schedulled_tasks()
        while(1):
            for name,TaskO in schedulled_tasks.items():
                if pycron.is_now(TaskO["cron"]):
                    os.environ["TASKNAME"] = name
                    logger_start(TaskO["function"])()
                    while pycron.is_now(TaskO["cron"]):pass

            sleep(1)
        pass


    def current_task_info(task=None):
        task_name = os.environ["TASKNAME"] if not task else task
        if task_name not in Task.schedulled_tasks(): return None
        
        bot = BotInfo.query().filter_by(botid=botConfig.BOT_ID).all()
        if not bot:
            raise Exception("BOT nao cadastrado!")
        if bot[0].botname != botConfig.BOT_NAME:
            raise Exception(f"BOTID '{botConfig.BOT_ID}' não corresponde a '{botConfig.BOT_NAME}'")
        
        current_task = [x for x in bot if x.task_name == task_name]
        if not current_task:
            raise Exception(f"TASK '{task_name}' inexistente!")
        return current_task[0]
