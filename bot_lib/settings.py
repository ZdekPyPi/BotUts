import json
import os
# PEGANDO CONFIGURACOES DO BOT ATUAL


class botConfig:
    BOT_NAME    : str  = os.getenv("BOT_NAME")
    BOT_ID      : str  = os.getenv("BOT_ID")
    MODE        : str  = os.getenv("MODE","DEV")

    @property
    def is_in_prd(self):
        return self.MODE == "PRD"

    def __repr__(self):
        return f"<botConfig {self.BOT_NAME}>"

botConfig = botConfig()