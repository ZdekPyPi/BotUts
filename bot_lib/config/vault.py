from vaultUts import VaultLib
import bot_lib
from bot_lib.settings import botConfig

vlt = VaultLib(botConfig.VAULT_HOST,botConfig.VAULT_TOKEN,in_prd=bot_lib.IN_PRD)


@vlt.link("Bot/data/Default2",switch_env_keys=True)
class BotVault(): 
    DB_HOST      : str
    DB_PWD       : str
    DB_USER      : str
    DB_NAME      : str
    SELENIUM_HOST: str
    USE_SELENOID : bool

@vlt.link("Slack/data/auth")
class SlackVault(): 
    TOKEN      : str




#BotVault.DB_HOST = '10.10.0.8'