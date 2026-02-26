from loguru import logger,_Logger
from bot_lib.database.orm import Log
import json
import sys
from bot_lib import botConfig
import os
from dateUts import now

class configLogger:
    HAS_WARNING, HAS_ERROR = False,False
    logger_path = None

    def __init__(self, logger_path):
        self.logger_path = logger_path
        #====================== AJUSTE DE QUEBRA DE LINHA DO LOG
        self.log = logger.patch(self.flatten_message)
        #===================== HABILITA AS CORES NO TERMINAL
        self.log.opt(colors=True)
        #=====================  CONFIGURACAO DA FORMATAÇÃO DAS MENSAGENS
        self.log = self.log.bind(line_exec="",func_name="",file_name="",time_exec="")
        #===================== REMOVE OS HANDLERS PADROES DO LOGURU
        self.log.remove()
        #===================== ADCIONA HANDDLERS
        self.add_handlers()

    @staticmethod
    def flatten_message(record):
        record["message"] = record["message"].replace("\n", " ").replace("{","{{").replace("}","}}")
    
    #====================== AJUSTE DE NOME DE ARQUIVO DOS LOGS
    @staticmethod
    def rename_rotated_file(filepath):
        new_path = os.path.dirname(filepath) + f"/{now(fmt='%Y-%m-%d_T_%H-%M-%S')}.log"
        os.rename(filepath, new_path)

    #===================== FORMATO DE MENSAGEM
    @staticmethod
    def formatter(record):
        extraReplace = lambda key,key2,tam: f"{{extra[{key}]: ^{tam}}}" if record.get("extra") and record.get("extra").get(key) else f"{{{key2}: ^{tam}}}"
        extraOpt = lambda key,tam: f"{{extra[{key}]: ^{tam}}}" if record.get("extra") and record.get("extra").get(key) else f"{' '*tam}"

        task= os.getenv("TASKNAME",'')
        fmt = [
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: ^8}</level>",
            f"{task: ^15}",
            extraReplace("file_name","file",15),
            extraReplace("func_name","function",15),
            extraReplace("line_exec","line",4),
            extraOpt("extra_1",15),
            "<level>{message}</level>"
        ]
        return " | ".join(fmt) + "\n"

    #====================== MARCA QUANDO A EXECUCAO TEVE WARNING
    def warning_error(self, record):
        data = json.loads(record)["record"]
        if data["level"]['name'] == 'WARNING':
            self.HAS_WARNING = True
        else:
            self.HAS_ERROR = True

    @staticmethod
    def handler_db(data):
        if not botConfig.is_in_prd: return
        data2 = json.loads(data)["record"]
        extra = data2["extra"]
        args = {
            "date"    : dt.strptime(data2["time"]["repr"],"%Y-%m-%d %H:%M:%S.%f%z"),
            #"date"    : fmtDate(dt.strptime(data2["time"]["repr"],"%Y-%m-%d %H:%M:%S.%f%z"),fmt="sql+hr"),
            "function": extra["func_name"] or data2["function"],
            "level"   : data2["level"]["name"],
            "file"    : extra["file_name"] or data2["file"]["name"],
            "module"  : data2["module"],
            "path"    : data2["name"],
            "line"    : extra["line_exec"] or data2["line"],
            "message" : data2["message"],
            "extra_1" : extra.get("extra_1")
        }
        Log(**args).save()

    def add_handlers(self):
        #===================== HANDLER DE ARQUIVO - GERA UM ARQUIVO POR DIA
        self.log.add(
            self.logger_path, 
            format="{time:YYYY-MM-DD HH:mm:ss} | {file: ^20} | {function: ^15} | {line: ^4} | {extra[file_name]: ^20} | {extra[func_name]: ^15} | {extra[line_exec]: ^4} | {level: ^8} | {message}",
            #format="{extra[line]}",
            rotation='00:00:00',
            serialize=False, 
            encoding='utf-8',
            compression=self.rename_rotated_file
            )
        #===================== HANDLER DO TERMINAL DE COMANDO
        self.log.add(
            sys.stdout,
            colorize=True,
            #format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: ^8}</level> | {file: ^20} | {function: ^15} | {line: ^4} | {extra[file_name]: ^20} | {extra[func_name]: ^15} | {extra[line_exec]: ^4} | <level>{message}</level>",
            format = self.formatter,
            backtrace=True,
            diagnose=True
        )
        #===================== HANDLER DO WARNING/ERROR
        self.log.add(
            self.warning_error,
            serialize=True,
            filter=lambda r:r["level"].name in ["WARNING","ERROR"]
        )
        #===================== HANDLER DO BANCO DE DADOS
        self.log.add(self.handler_db,serialize=True)

    def re_start(self):
        open(LOGGER_PATH,"a").write(f"#{'='*200}\n")
        self.HAS_ERROR, self.HAS_WARNING = False,False

class configLevels:
    n_level = 0

    def __init__(self):
        self.log.level("BUSNSEXP", no=25, color="<magenta>")
        self.log.level("INTER",    no=30, color="<cyan><bold>") #POSIVEIS CORES -> https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.level
        self.log.level("JOB",      no=35, color="<light-blue><bold>")

    def set_level(self,log_level=0):
        self.n_level = log_level

    def reset_level(self):
        self.n_level = 0

    def bind_extra(self,extra):
        self._options = self.log.bind(extra_1=extra)._options

    def success(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).success(f"{tabs}{message}",**kwargs)
    
    def info(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).info(f"{tabs}{message}",**kwargs)
    
    def warning(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).warning(f"{tabs}{message}",**kwargs)
    
    def error(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).error(f"{tabs}{message}",**kwargs)
    
    def critical(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).critical(f"{tabs}{message}",**kwargs)
    
    def busnsexp(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).log("BUSNSEXP",f"{tabs}{message}",**kwargs)
    
    def exception(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).exception(f"{tabs}{message}",**kwargs)

    def debug(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).debug(f"{tabs}{message}",**kwargs)
            
    def inter(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).log("INTER",f"{tabs}{message}",**kwargs)
    
    def job(self,message,log_level=0,depth = 1,**kwargs):
        level = log_level if log_level else self.n_level
        tabs = "\t" * level
        self.log.opt(depth=depth).log("JOB",f"{tabs}{message}",**kwargs)


class customLogger(configLogger,configLevels):
    def __init__(self,logger_path):
        configLogger.__init__(self, logger_path)
        configLevels.__init__(self)

    


