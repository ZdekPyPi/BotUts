from bot_lib import *



@Task.config(task_name="test", local=True)
def main():
    logger.info("Teste de log")
    mark_inter(10, "Teste de marcação INTER")
    mark_job("PASTA", "Teste de marcação JOB")


if __name__ == "__main__":
    Task.run_task("test")
 