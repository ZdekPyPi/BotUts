from sqlalchemy import cast, Date, desc
from datetime import date
from dateUts import now, today
import sqlalchemy as sa
import platform
import psutil
import socket
import os
if not "Windows" in platform.platform():
    import pwd
from sqlalchemy import func
from bot_lib.settings import botConfig
import bot_lib
from bot_lib.database.base import Base


class Log(Base):
    __tablename__ = 'tbs_logs'
    # __table_args__ = {"schema": 'python'}

    id_proc = sa.Column(sa.Integer)
    datetime = sa.Column(sa.DateTime, nullable=False)
    botname = sa.Column(sa.String(100), nullable=False)
    botid = sa.Column(sa.String(100), nullable=False)
    task_name = sa.Column(sa.String(100))
    level = sa.Column(sa.String(50), nullable=False)
    function = sa.Column(sa.String(100))
    message = sa.Column(sa.TEXT)
    extra_1 = sa.Column(sa.TEXT)
    file = sa.Column(sa.String(100))
    path = sa.Column(sa.String(100))
    module = sa.Column(sa.String(100))
    line = sa.Column(sa.Integer)
    hostname = sa.Column(sa.String(100), nullable=False)
    user_pc = sa.Column(sa.String(255), nullable=False)
    ram = sa.Column(sa.Float, nullable=False)
    ram_available = sa.Column(sa.Float, nullable=False)
    cpu_usage_percent = sa.Column(sa.Float, nullable=False)

    def __init__(self, level, date=None, function=None, file=None,
                 module=None, path=None, line=None, message=None, extra_1=None):
        self.user_pc = os.getlogin() if "Windows" in platform.platform(
        ) else pwd.getpwuid(os.getuid())[0]
        self.cpu_usage_percent = psutil.cpu_percent()
        self.ram = round(psutil.virtual_memory().total / 1000000000, 0)
        self.ram_available = round(
            psutil.virtual_memory().available / 1000000000, 0)
        self.hostname = socket.gethostname()
        self.datetime = now().date if not date else date
        self.function = function
        self.level = level
        self.message = message
        self.extra_1 = extra_1
        self.file = file
        self.module = module
        self.path = path
        self.line = line
        self.botname = botConfig.BOT_NAME
        self.botid = botConfig.BOT_ID
        self.id_proc = self.get_id_proc()
        self.task_name = os.getenv("TASKNAME")

    def get_id_proc(self):
        if self.level in ('DEBUG', 'CRON'):
            return None

        idprc = os.getenv("ID_PROC")

        if not idprc:
            # lg = Log.query().filter(cast(Log.datetime,Date) == date.today(),Log.botname == botConfig.BOT_NAME).filter(Log.id_proc != None).order_by(desc(Log.id_proc)).first()
            lg = Log.query().filter(
                func.date(
                    Log.datetime) == today("sql"),
                Log.botname == botConfig.BOT_NAME).filter(
                Log.id_proc is not None).order_by(
                desc(
                    Log.id_proc)).first()
            if not lg or lg.id_proc is None:
                os.environ["ID_PROC"] = "0"
            else:
                os.environ["ID_PROC"] = str(lg.id_proc + 1)
        return int(os.environ["ID_PROC"])
