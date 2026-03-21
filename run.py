from bot_lib import *
from bot_lib.cli import *

@Task.new(name="test", local=True)
def main():
    logger.info("Etapa 1")
    #DO SOMETHING
    logger.info("Etapa 2")
    #DO SOMETHING


if __name__ == "__main__":
    main()