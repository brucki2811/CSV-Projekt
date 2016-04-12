from abc import ABCMeta

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class Connector(metaclass=ABCMeta):
    def __init__(self, conn):
        db = conn
        self.engine = create_engine(db)
        connect = self.engine.connect()
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)
        self.classes = Base.classes

    def getSession(self):
        return self.session

    def getConnection(self):
        return self.engine.raw_connection()

    def getClass(self, entity):
        return getattr(self.classes, entity)


class MySQLConnector(Connector):
    def __init__(self, username, password, database):
        connection_string = "mysql+mysqldb://" + username + ":" + password + "@localhost/" + database + "?charset=utf8"
        super().__init__(connection_string)
