from bot_lib import *

@Task.config(task_name="test", local=True)
def main():
    logger.info("Etapa 1")
    #DO SOMETHING
    logger.info("Etapa 2")
    #DO SOMETHING


if __name__ == "__main__":
    Task.run_task("test")