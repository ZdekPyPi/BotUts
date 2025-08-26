from sqlalchemy import String
import sqlalchemy as sa
from bot_lib.database.base import Base

class BotInfo(Base):
    __tablename__ = 'tbs_bots_info'
    __table_args__ = {'schema': 'python'}

    botid            = sa.Column(String(10))
    status           = sa.Column(String(50))
    bottitle         = sa.Column(String(100))
    botname          = sa.Column(String(100))
    task_name        = sa.Column(String(100))
    area             = sa.Column(String(50))
    squad            = sa.Column(String(50))
    key_users        = sa.Column(String)
    key_users_emails = sa.Column(String)
    notify_emails    = sa.Column(String)
    observacao       = sa.Column(String)
