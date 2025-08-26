from dateUts import now
import sqlalchemy as sa
import platform
import psutil
import socket
import os
if not "Windows" in platform.platform(): import pwd
from bot_lib.database.base import Base
from bot_lib.settings import botConfig

# =========================== API MONITOR ==============================================================
class ApiMonitor(Base):
    __tablename__ = 'api_monitor'
    __table_args__ = {"schema": 'python'}

    id_proc           = sa.Column(sa.Integer)
    datetime          = sa.Column(sa.DateTime,nullable=False)
    botname           = sa.Column(sa.String(100),nullable=False)
    botid             = sa.Column(sa.String(100),nullable=False)
    method            = sa.Column(sa.String(50),nullable=False)
    function          = sa.Column(sa.String(100))
    url               = sa.Column(sa.String(255))
    host              = sa.Column(sa.String(255))
    url_path          = sa.Column(sa.String(255))
    time_exec         = sa.Column(sa.Integer)
    status_code       = sa.Column(sa.Integer)
    message           = sa.Column(sa.TEXT)
    file              = sa.Column(sa.String(100))
    path              = sa.Column(sa.String(100))
    module            = sa.Column(sa.String(100))
    line              = sa.Column(sa.Integer)
    hostname          = sa.Column(sa.String(100),nullable=False)
    user_pc           = sa.Column(sa.String(255),nullable=False)
    ram               = sa.Column(sa.Float,nullable=False)
    ram_available     = sa.Column(sa.Float,nullable=False)
    cpu_usage_percent = sa.Column(sa.Float,nullable=False)


    def __init__(self,method,date=None,function=None,url=None,host=None,url_path=None,time_exec=None,status_code=None,file=None,module=None,path=None,line=None,message=None):
        self.user_pc           = os.getlogin() if "Windows" in platform.platform() else pwd.getpwuid(os.getuid())[0]
        self.cpu_usage_percent = psutil.cpu_percent()
        self.ram               = round(psutil.virtual_memory().total/1000000000, 0)
        self.ram_available     = round(psutil.virtual_memory().available/1000000000, 0)
        self.hostname          = socket.gethostname()
        self.datetime          = now().date if not date else date
        self.function          = function
        self.method            = method
        self.time_exec         = time_exec
        self.message           = message
        self.file              = file
        self.module            = module
        self.path              = path
        self.line              = line
        self.botname           = botConfig.BOT_NAME
        self.botid             = botConfig.BOT_ID
        self.id_proc           = os.getenv("ID_PROC",None)
        self.url               = url
        self.host              = host
        self.url_path          = url_path
        self.status_code       = status_code

