import os
from dotenv import load_dotenv
import urllib3
import pathlib
from .logger import customLogger
import platform

#===================== LIMPA O TERMINAL DE COMANDO
os.system("cls" if "Windows" in platform.platform() else "clear")

#CRIA AS PASTAS VAZIAS
if not os.path.isdir("./logs"): os.makedirs("./logs") 
if not os.path.isdir("./temp"): os.makedirs("./temp")

#VARIAVEIS DE AMBIENTE DEFAULT
lib_folder = pathlib.Path(__file__).parent.resolve()
load_dotenv(f"{lib_folder}/_.env",override=False)

#VARIAVEIS DE AMBIENTE DO PROJETO
load_dotenv(f".env",override=True)

#DESLIGA OS WARNNINGS DE SSL
urllib3.disable_warnings()


#INICIA O LOGGER
logger  = customLogger("./logs/current.log")