import tkinter

import pandas
import seaborn as sns
import matplotlib.pyplot as plt

import Utils.Utils as utl
from tkinter import filedialog
from tkinter import Tk


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

    print("Total: " + str(valid) + ", " + str(mssq))
    return {"valid": valid, "mssq": mssq}


def scoreMSSQPart(data: pandas.Series, cutoff: int) -> dict:
    dl = len(data.index)
    t = 0  # not applicable
    ss = 0  # Sickness Score

    for d in data:
        if d == "t":
            t += 1
        else:
            ss += int(d)

    msx = (ss * dl) / (dl - t)
    val = t < cutoff
    print(">    NA: " + str(t))
    print(">    SS: " + str(ss))
    print(">   MSx: " + str(ss))
    print("> Valid: " + str(val))

    return {"valid": val, "mssq": msx}


def importMSSQ():
    Tk().withdraw()
    file_path = filedialog.askopenfile(filetypes=[("CSV", "*.csv; *.CSV")]).name
    print(file_path)

    mssq_collection = {}
    try:
        mssq_collection = pandas.read_csv(file_path, sep=";", index_col=0)
    except pandas.errors.EmptyDataError:
        print("file is empty")
        mssq_collection = pandas.DataFrame()

    mssq = scoreMSSQ(utl.readCSV(), 5)
    mssq_collection[input("name:\n")] = mssq
    mssq_collection.to_csv(file_path, sep=";")


def main():
    importMSSQ()


if __name__ == "__main__":
    main()
