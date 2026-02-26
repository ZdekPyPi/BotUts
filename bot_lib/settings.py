from dotenv import load_dotenv
import json
import os

# VARIAVEIS DE AMBIENTE DO PROJETO
load_dotenv(f".env", override=True)


class botConfig:
    BOT_NAME: str  = os.getenv("BOT_NAME")
    BOT_ID  : str  = os.getenv("BOT_ID")
    MODE    : str  = os.getenv("MODE", "DEV")
    LOG_DB  : bool = os.getenv("LOG_DB", "N").upper() == "Y"

    @property
    def is_in_prd(self):
        return self.MODE == "PRD"

    def __repr__(self):
        return f"<botConfig {self.BOT_NAME}>"


botConfig = botConfig()
