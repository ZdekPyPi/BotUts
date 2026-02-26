# TEST FILE
from bot_lib import botConfig
from bot_lib import mark_inter, commit_mark_inter, mark_job
from bot_lib import *
from bot_lib.settings import *
from bot_lib.cli import *
import sys
sys.path.append("./bot_lib")


# botlib_commands()
# run_prd()
# run_prd_stream()
# create_stack()
# pull_redeploy()

# sys.exit()


print(botConfig.BOT_NAME)
print(botConfig.BOT_ID)
print(botConfig.MODE)
print(botConfig.is_in_prd)


@Task.config(task_name="test", local=True)
def main():
    logger.info("Teste de log")
    mark_inter(10, "Teste de marcação INTER")
    mark_job("PASTA", "Teste de marcação JOB")


if __name__ == "__main__":
    Task.run_task("minha_task")
