from dotenv import load_dotenv
import urllib3
import os
import pathlib

#CARREGA VARIAVEIS DE AMBIENTE

lib_folder = pathlib.Path(__file__).parent.resolve()
load_dotenv(f"{lib_folder}/_.env",override=False)
load_dotenv(f".env",override=False)
#os.environ["MODE"] = 'PRD'

LOGGER_PATH = "./logs/current.log"


#DESLIGA OS WARNNINGS DE SSL
urllib3.disable_warnings()


#Define o Mode
IN_PRD = os.getenv("MODE","DEV")=="PRD"





