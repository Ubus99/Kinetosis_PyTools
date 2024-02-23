from tkinter import Tk

import sqlalchemy
from sqlalchemy import MetaData

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

    # db.metadata.create_all(db.engine)  # executes previously  registered statements


if __name__ == "__main__":
    main()
