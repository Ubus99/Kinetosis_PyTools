import os
import tkinter

import numpy as np
import pandas
import seaborn as sns
import matplotlib.pyplot as plt

import Utils.Utils as utl
from tkinter import filedialog
from tkinter import Tk


def sanitizeCSV(df: pandas.DataFrame) -> pandas.DataFrame:
    print("sanitizer input:")
    print(df)
    df.columns = df.columns.str.replace(' ', '')
    df = df.replace(r"^ +| +$", r"", regex=True)
    return df.drop_duplicates(subset='tobii_timestamp').iloc[1:]


def calculateHeatmap(df: pandas.DataFrame, res: int):
    print("heatmap input:")
    print(df)

    print("init grid")
    grid = np.zeros(shape=[res, res], dtype=int)

    print("init Dict")
    dict_unscaled = {}

    print("load vectors")
    for e in df.index:
        idx = df["tobii_timestamp"][e]
        print("-> " + str(idx) + ":")
        # load floats into vector
        x = float((df["GazeX"][e]).replace(",", ".")) + 0.5
        y = float((df["GazeY"][e]).replace(",", ".")) + 0.5
        v = np.array([x, y]).clip(0, 1)
        dict_unscaled[idx] = v

        # put vectors into buckets
        v_s = v * res
        print("scaled >\t" + str(v_s))
        v_int = np.rint(v_s).astype(int)
        print("rounded >\t" + str(v_int))
    print()

    print("map:")
    print(grid)
    return grid


def importData():
    Tk().withdraw()

    # load input
    file_paths = filedialog.askopenfiles(
        initialdir="./Data", filetypes=[("CSV", "*.csv; *.CSV")], title="Select Data"
    )

    # load output
    try:
        database_path = filedialog.askopenfile(
            initialdir="./", filetypes=[("CSV", "*.csv; *.CSV")], title="Select Database"
        ).name
        database_df = utl.readCSV(database_path)

    except pandas.errors.EmptyDataError:
        print("file is empty")
        database_df = pandas.DataFrame()

    # process input
    for p in file_paths:
        path = p.name
        map = calculateHeatmap(sanitizeCSV(utl.readCSV(path)), 11)


def main():
    importData()


if __name__ == "__main__":
    main()
