import json
import bot_lib

# PEGANDO CONFIGURACOES DO BOT ATUAL
setup = json.load(open('settings.json'))
setup = {**setup["PRD"],**(setup["DEV"] if not bot_lib.IN_PRD else {})}


class botConfig:
    BOT_NAME    : str  = setup["BOT_NAME"]
    BOT_ID      : str  = setup["BOT_ID"]
    VAULT_HOST  : str  = setup["VAULT_HOST"]
    VAULT_TOKEN : str  = setup["VAULT_TOKEN"]
    RAW         : dict = setup

    def __repr__(self):
        return f"<botConfig {self.BOT_NAME}>"

botConfig = botConfig()

pass