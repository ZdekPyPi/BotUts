from sqlalchemy.ext.declarative import declarative_base, declared_attr
from bot_lib.database.db import DbBot
import sqlalchemy as sa


class CustomBase:

    id = sa.Column(sa.Integer,primary_key=True,autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    # Acesso direto a queries: Model.query
    @classmethod
    def query(cls):
        return DbBot().query(cls)
    
    def add(self):
        if not self.id:
            DbBot().add(self)

    def save(self):
        try:
            s = DbBot()
            if not self.id:
                s.add(self)
            s.commit()
        except:
            s.rollback()
            raise

    def delete(self):
        s = DbBot()
        s.rollback()
        s.delete(self)
        s.commit()


# base que adciona os metodos Save, Delete
Base = declarative_base(cls=CustomBase)