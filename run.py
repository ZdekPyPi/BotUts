#TEST FILE
import sys
sys.path.append("./bot_lib")

from bot_lib.cli import *
from bot_lib.settings import *


#botlib_commands()
#run_prd()
#run_prd_stream()
#create_stack()
#pull_redeploy()

#sys.exit()

from bot_lib import *



@Task.config(task_name="test",local=True)
def main():
    logger.info("Teste de log")
    mark_inter(10,"Teste de marcação INTER")
    mark_job("PASTA","Teste de marcação JOB")

terminal_opt()