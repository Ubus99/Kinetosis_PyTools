import os.path
from tkinter import Tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
import pandas
import seaborn as sns

import Utils.Utils as utl


def sanitizeCSV(df: pandas.DataFrame) -> pandas.DataFrame:
    print("sanitizer input:")
    print(df)
    df.columns = df.columns.str.replace(' ', '')
    df = df.replace(r"^ +| +$", r"", regex=True)
    out = df.drop_duplicates(subset='tobii_timestamp').iloc[1:]

    return out


def preprocessor(df: pandas.DataFrame, res: int, overscan: int) -> pandas.DataFrame:
    print("preprocessor input:")
    print(df)

    print("loading vectors:")
    v_list = []

    for e in df.index:
        # load floats into vector
        x = float((df["GazeX"][e]).replace(",", ".")) + 0.5
        y = float((df["GazeY"][e]).replace(",", ".")) + 0.5
        v = np.array([x, y])  # .clip(0, 1)
        v_list.append(v)

    v_list = np.asarray(v_list)
    print(v_list)
    print()

    print("scaling vectors:")
    v_scaled = v_list * (res - (overscan + 1)) + (overscan / 2)  # for indexing
    v_scaled
    print(v_scaled)
    print()

    print("binning vectors:")
    v_int = np.rint(v_scaled).astype(int).clip(0, res - 1)
    print(v_int)
    print()

    print("compositing dataframe.")
    out = pandas.DataFrame(v_int, columns=["x", "y"])
    timestamp = df["tobii_timestamp"].to_list()
    out["timestamp"] = timestamp
    print()
    return out


def calculateHeatmap(df: pandas.DataFrame, res: int) -> np.ndarray:
    print("heatmap input:")
    # with pandas.option_context(
    # 'display.max_rows', None, 'display.max_columns', None, 'display.precision', 3
    # ):
    print(df)

    print("init grid")
    grid = np.zeros(shape=[res, res], dtype=float)

    print("map:")
    ms_ges = df["timestamp"].max() - df["timestamp"].min()

    for e in df.index:
        x = df["x"][e]
        y = df["y"][e]

        if e + 1 < len(df):
            ms = df["timestamp"][e + 1] - df["timestamp"][e]
        else:
            ms = df["timestamp"][e] - df["timestamp"][e - 1]
        grid[x][y] += (ms / ms_ges) * 100 * 100

    grid[grid < 1] = 1
    grid = np.log(grid)
    grid /= 100
    print(grid.round(2))
    return grid


def drawHeatmap(arr: np.ndarray):
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        arr, cmap=cmap, square=True, linewidths=.5, cbar_kws={"shrink": .5}, vmin=0
    )

    plt.show()


def importData():
    Tk().withdraw()

    res = 33

    # load input
    file_paths = filedialog.askopenfiles(
        initialdir="./Data", filetypes=[("CSV", "*.csv; *.CSV")], title="Select Data"
    )

    # process input
    for p in file_paths:
        # prep data
        path = p.name
        df_san = sanitizeCSV(utl.readCSV(path))
        df_prep = preprocessor(df_san, res, 10)

        # save prep data
        basename = os.path.basename(path).split('.')[0]
        dbpath = os.path.dirname(path) + "/" + basename + "_cleaned.csv"
        df_prep.to_csv(dbpath, sep=";")

        # visualize data
        mx = calculateHeatmap(df_prep, res)
        drawHeatmap(mx)


def main():
    importData()


if __name__ == "__main__":
    main()
