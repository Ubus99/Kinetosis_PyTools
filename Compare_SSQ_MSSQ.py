import os
from tkinter import Tk

import Utils.misc as utl
from Utils.CacheManager import CacheManager


def importMSSQ():
    Tk().withdraw()

    cache = CacheManager("compare_SSQ_MSSQ", "Lukas Berghegger")

    # load input
    ssq_paths = utl.multiLoadCSV(cache["ssqPath"], "select Data")
    cache["ssqPath"] = os.path.dirname(os.path.abspath(ssq_paths[0].name))

    mssq_path = utl.loadCSV(cache["mssqDatabasePath"], "select Data")
    cache["mssqDatabasePath"] = os.path.dirname(os.path.abspath(mssq_path.name))

    # load output

    # store output
    # print(mssq_collection)
    # print()
    # mssq_collection.sort_values(by="pct", axis="columns", inplace=True)
    # mssq_collection.to_csv(database_path, sep=";")


def main():
    importMSSQ()


if __name__ == "__main__":
    main()
