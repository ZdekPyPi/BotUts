from bot_lib.database.orm import Log
from bot_lib import botConfig
from bot_lib import logger

TO_COMMIT = []

def mark_inter(seconds:int,description:str="",commit=True):
    if botConfig.is_in_prd:
        if commit:
            Log(level="INTER",message=description,extra_1=str(seconds)).save()
        else:
            TO_COMMIT.append((seconds,description))
    logger.inter(description, extra_1=str(seconds))

def commit_mark_inter():
    for seconds,description in TO_COMMIT:
        Log(level="INTER",message=description,extra_1=str(seconds)).save()
    TO_COMMIT.clear()

def mark_job(type_job:str, description:str="", qtd:int=1):
    if botConfig.is_in_prd:
        Log(level="JOB",message=description,extra_1=str(qtd)).save()
    logger.job(f"({type_job}) - {description}", extra_1=str(qtd))