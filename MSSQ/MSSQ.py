import os
from tkinter import Tk

import pandas

import Utils.misc as utl
from Utils.CacheManager import CacheManager

MSSQ_25th = 5.0
MSSQ_50th = 11.5
MSSQ_75th = 19.0
MSSQ_Median = 12.9


def calcMSSQPercentile(MSSQ_Raw: float) -> float:
    a = 5.1160923
    b = -0.055169904
    c = -0.00067784495
    d = 0.000010714752
    pct = a * MSSQ_Raw + b * pow(MSSQ_Raw, 2) + c * pow(MSSQ_Raw, 3) + d * pow(MSSQ_Raw, 4)
    pct = round(pct, 2)
    return pct


def scoreMSSQ(data: pandas.DataFrame, cutoff: int) -> dict:
    print(data)

    print("Kind:")
    buff = scoreMSSQPart(data["Kind"], cutoff)
    mssq = buff["mssq"]
    valid = buff["valid"]

    print("Erwachsen:")
    buff = scoreMSSQPart(data["Erwachsen"], cutoff)
    mssq += buff["mssq"]
    valid |= buff["valid"]

    pct = calcMSSQPercentile(mssq)

    print("Total: " + str(valid) + ", " + str(mssq) + ", " + str(pct))
    return {"valid": valid, "mssq": float(mssq), "pct": float(pct)}


def scoreMSSQPart(data: pandas.Series, cutoff: int) -> dict:
    dl = len(data.index)
    t = 0  # not applicable
    ss = 0  # Sickness Score

    for d in data:
        if d == "t":
            t += 1
        else:
            ss += int(d)

    msx = round((ss * dl) / (dl - t), 2)
    valid = t <= cutoff
    pct = calcMSSQPercentile(msx)

    print(">         NA: " + str(t))
    print(">         SS: " + str(ss))
    print(">        MSx: " + str(msx))
    print("> percentile: " + str(pct))
    print(">      Valid: " + str(valid))

    return {"valid": valid, "mssq": float(msx)}


def importMSSQ():
    Tk().withdraw()

    cache = CacheManager("MSSQ", "Lukas Berghegger")

    # load input
    mssq_paths = utl.multiLoadCSV(cache["dataPath"], "select Data")
    cache["dataPath"] = os.path.dirname(os.path.abspath(mssq_paths[0].name))

    # load output
    try:
        database_path = utl.loadCSV(cache["databasePath"], "select Database")
        mssq_collection = utl.parseCSV(database_path)
        cache["databasePath"] = os.path.dirname(os.path.abspath(database_path))

    except pandas.errors.EmptyDataError:
        print("file is empty")
        mssq_collection = pandas.DataFrame()

    # process input
    for p in mssq_paths:
        path = p.name
        mssq = scoreMSSQ(utl.parseCSV(path), 2)

        mssq_collection[os.path.basename(path).removesuffix(".csv")] = mssq
        mssq_collection.loc["pct"] = mssq_collection.loc["pct"].astype(float)

    # store output
    print(mssq_collection)
    print()
    mssq_collection.sort_values(by="pct", axis="columns", inplace=True)
    mssq_collection.to_csv(database_path, sep=";")


def main():
    importMSSQ()


if __name__ == "__main__":
    main()
