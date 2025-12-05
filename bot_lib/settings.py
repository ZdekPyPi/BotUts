import json
import bot_lib
import os
# PEGANDO CONFIGURACOES DO BOT ATUAL


class botConfig:
    BOT_NAME    : str  = os.getenv("BOT_NAME")
    BOT_ID      : str  = os.getenv("BOT_ID")
    VAULT_HOST  : str  = os.getenv("VAULT_HOST")
    VAULT_TOKEN : str  = os.getenv("VAULT_TOKEN")

    def __repr__(self):
        return f"<botConfig {self.BOT_NAME}>"

botConfig = botConfig()