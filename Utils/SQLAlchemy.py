from tkinter import Tk

import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from SSQ.SSQ_Class import SSQ
from Utils.CacheManager import CacheManager


class SQLAlchemyHelper:

    def __init__(self, path: str = ":memory:", log: bool = False):  # todo is path connection correct?
        self.engine = sqlalchemy.create_engine("sqlite+pysqlite:///" + path, echo=log)
        self.metadata = sqlalchemy.MetaData()

    def InitTable(self, metadata: MetaData):
        metadata.create_all(self.engine)  # todo does overwrite?


def main():
    Tk().withdraw()

    cache = CacheManager("SQLAlchemyHelper", "Lukas Berghegger")
    # path = filedialog.askopenfile(
    #     initialdir=str(cache["path"]),
    #     filetypes=[("SQLite", "*.db")],
    #     title="load Database"
    # ).name
    # cache["path"] = path

    db = SQLAlchemyHelper("../test.db", True)

    db.InitTable(SSQ.metadata)
    ssq1 = SSQ(n=0.1, o=0.1, p=0.1, ts=0.1)

    print(ssq1)
    session = Session(db.engine)
    session.add(ssq1)
    session.flush()
    session.commit()

    # db.metadata.create_all(db.engine)  # executes previously  registered statements


if __name__ == "__main__":
    main()
