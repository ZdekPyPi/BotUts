import sys
import os
from functools import wraps
from bot_lib.config import logger
from bot_lib.errors import *
from .task import Task
import bot_lib
from time import time
from bot_lib.libs import mark
BEFORE_START_EVENT = []
AFTER_FINISH_EVENT = []

task_time_start = None
task_time_end   = None

def elapsed_time():
    global task_time_start,task_time_end
    return round((time() if task_time_end is None else task_time_end) - task_time_start,2)

def replace_chars(text):
    chars = ["{","}"]
    for ch in chars:
        text = text.replace(ch, ch*2)
    return text

def before_start_event(function): #ANTES DE INICIAR
    global BEFORE_START_EVENT
    function.__EVENTTYPE__ = "<BF_ST_EVT>"
    BEFORE_START_EVENT.append(logger_manager(function))

    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
        
    return wrapper

def after_finish_event(function): #DEPOIS DE TERMINAR
    global AFTER_FINISH_EVENT
    function.__EVENTTYPE__ = "<AF_FI_EVT>"
    AFTER_FINISH_EVENT.append(logger_manager(function))
    
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            raise EventException(str(e))
        
    return wrapper

def logger_start(function):
    Task.current_task_info(function.__TASKNAME__)
    @wraps(function)
    def wrapper(*args, **kwargs):
        global task_time_start,task_time_end
        os.environ.pop("ID_PROC", None)
        try:
            os.environ["TASKNAME"] = function.__TASKNAME__
            logger.bind_extra(None) #RESETA O BIND
            logger.info(f"========== TASK({function.__TASKNAME__}) ===========",depth=3)

            logger.success("START",func_name = function.__name__,depth=3)

            #BEFORE START EVENT
            if BEFORE_START_EVENT:[fn() for fn in BEFORE_START_EVENT]

            #METODOS PARA CALCULO DO TEMPO DE EXECUÇÃO
            task_time_start = time()

            logger_manager(function)(*args, **kwargs)
            task_time_end= time()
            
            logger.bind_extra(None) #RESETA O BIND

            #AFTER FINISH EVENT
            if AFTER_FINISH_EVENT:[fn("WARNING" if logger.HAS_WARNING else "SUCCESS","") for fn in AFTER_FINISH_EVENT]

            fnc = logger.warning if logger.HAS_WARNING else logger.success
            fnc("FINISHED",func_name = function.__name__,depth=3)
        except BusinessException as e: 
            if AFTER_FINISH_EVENT:[fn("BUSNSEXP",str(e)) for fn in AFTER_FINISH_EVENT]
            logger.log("BUSNSEXP", "FINISHED",func_name = function.__name__,depth=3)
            pass
        #except ValueError       : logger.error("FINISHED",func_name = function.__name__)
        except Exception   as e: 
            if AFTER_FINISH_EVENT:[fn("CRITICAL",str(e)) for fn in AFTER_FINISH_EVENT]
            logger.critical("FINISHED",func_name = function.__name__,depth=3)
        except EventException  as e:                                    # QUANDO FOR UM EVENTO QUE DEU ERRO NAO PODE CHAMAR OS EVENTOS NOVAMENTE SE CAIR EM EXCEPTION
            logger.critical("FINISHED",func_name = function.__name__,depth=3)
        finally:
            bot_lib.ID_PROC    = None
            logger.HAS_ERROR   = None
            logger.HAS_WARNING = None
            mark.TO_COMMIT     = []
            os.environ.pop("ID_PROC", None) 
            os.environ.pop("TASKNAME", None) 

    return wrapper

def logger_manager(function):
    file_name = os.path.basename(function.__code__.co_filename)
    params = lambda : {"line_exec":sys.exc_info()[2].tb_next.tb_lineno if sys.exc_info()[2].tb_next else None,"func_name":function.__name__,"file_name":file_name}

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
           return function(*args, **kwargs)
        except BusinessException as e:
            logger.log("BUSNSEXP", str(e))
            raise
        except Exception as e:
            if "__EVENTTYPE__" in function.__dict__: # SE A FUNCAO FOR DO TIPO EVENTO
                logger.critical(replace_chars(str(e)),**params(),extra_1=function.__EVENTTYPE__)
                raise EventException(str(e))
            else:    
                logger.critical(replace_chars(str(e)),**params())
                raise
    return wrapper

def logger_class():
    def wraps(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, logger_manager(getattr(cls, attr)))
        return cls
    return wraps

