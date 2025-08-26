from .loguru import *
from .api_monitor import *
from .task import *
from sys import argv
from bot_lib.common.colorama_print import print_with_color_tags
import bot_lib

def print_table(data):
    if not data:
        print("=============SEM TASKS=============")
        return
    
    # Obtém as chaves do primeiro dicionário como cabeçalhos
    headers = list(data[0].keys())
    
    # Calcula a largura máxima de cada coluna
    col_widths = {key: max(len(str(row.get(key, ''))) for row in data) for key in headers}
    col_widths = {key: max(col_widths[key], len(key)) for key in headers}  # Considera o tamanho do cabeçalho
    
    # Imprime o cabeçalho
    header_row = " | ".join(f"{key.ljust(col_widths[key])}" for key in headers)
    print_with_color_tags(f"<black><bg_white> {header_row} </bg_white></black>")
    #print(header_row)
    #print("-" * len(header_row))
    
    # Imprime os dados
    for row in data:
        print(''," | ".join(f"{str(row.get(key, '')).ljust(col_widths[key])}" for key in headers),' ')


def show_tasks():
    tasks = Task.TASKS
    print_table([{"name":k,**{x:v[x] for x in v if x != "function"}} for k,v in tasks.items()])
    return


def terminal_opt():
    tasks = Task.TASKS
    if not tasks:
        raise Exception("Sem tasks configuradas!")

    if len(argv) >1:
        command = argv[1]

        if command == "config":
            return bot_lib.libs.show_config()
        if command == "tasks":
            return show_tasks()
        elif command == "run_all":
            for task in tasks:
                logger_start(tasks[task]["function"])()
        elif command in tasks:
            logger_start(tasks[command]["function"])()
        else:
            print(f"Task/Command '{command}' not found!")
        
    else:
        #EXECUTA A PRIMEIRA TASK CASO NENHUMA SEJA PASSADA
        task = list(tasks.keys())[0]
        logger_start(tasks[task]["function"])()