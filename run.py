#TEST FILE
import sys
sys.path.append("./bot_lib")

from bot_lib.cli import *
from bot_lib.settings import *


botlib_commands()
#run_prd()
#run_prd_stream()
#create_stack()
#pull_redeploy()

sys.exit()

from bot_lib import *


from bot_lib.settings import *
from bot_lib.logger.logger_db import *
from bot_lib.database.orm import *
from bot_lib.database.db import GetDbBot
from bot_lib.logger.loguru import *
from bot_lib.libs import show_config
from bot_lib.libs.loguru import before_start_event, logger_start

pass
ApiMonitor.query


@logger_start
def main():
    pass

main()