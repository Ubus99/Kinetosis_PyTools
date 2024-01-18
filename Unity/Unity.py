import os.path
from tkinter import Tk

import matplotlib.pyplot as plt
import numpy as np
import pandas
import seaborn as sns

import Utils.Utils as utl
from Utils.Cache_Handler import CacheHandler


def sanitizeCSV(df: pandas.DataFrame) -> pandas.DataFrame:
    print("sanitizer input:")
    print(df)
    df.columns = df.columns.str.replace(' ', '')
    df = df.replace(r"^ +| +$", r"", regex=True)
    df = df.drop_duplicates(subset='tobii_timestamp').iloc[1:]

    mode = df["Mode"]
    mode.reset_index(drop=True, inplace=True)
    mode.apply(lambda s: str(s).strip())
    mode.where(
        mode != "",
        other=None,
        inplace=True
    )
    a = mode.first_valid_index()
    out = df.iloc[a:]

    return out


def preprocessor(df: pandas.DataFrame, res: int) -> pandas.DataFrame:
    print("preprocessor input:")
    print(df)

    print("loading vectors:")
    v_list = []

    for e in df.index:  # load floats into vector
        x = float((df["GazeX"][e]).replace(",", "."))
        y = float((df["GazeY"][e]).replace(",", "."))
        v = np.array([x, y])
        v_list.append(v)

    v_list = np.asarray(v_list)  # import list
    print(v_list)
    print()

    print("fitting vectors:")
    v_mag = np.linalg.norm(v_list, axis=1) * 2  # get magnitude of all vectors
    v_scaled = v_list / v_mag.max()  # scale such that the largest vector has magnitude 1
    v_scaled += 0.5
    print(v_scaled)
    print()

    print("scaling vectors:")
    v_scaled *= (res - 1)  # scale to fit matrix
    print(v_scaled)
    print()

    print("binning vectors:")
    v_int = np.rint(v_scaled).clip(0, res - 1).astype(int)
    print(v_int)
    print()

    print("compositing dataframe.")
    out = pandas.DataFrame(v_int, columns=["x", "y"])
    timestamp = df["tobii_timestamp"].astype(int).to_list()
    out["timestamp"] = timestamp
    print()
    return out


def calculateHeatmap(df: pandas.DataFrame, res: int) -> pandas.DataFrame:
    print("heatmap input:")
    print(df)

    print("init grid")
    grid = np.zeros(shape=[res, res], dtype=float)
    grid = pandas.DataFrame(grid)

    print("map:")
    for e in df.index:
        x = df["x"][e]
        y = df["y"][e]

        if e + 1 < len(df):  # get gaze duration
            ms = df["timestamp"][e + 1] - df["timestamp"][e]
        else:  # catch end of array
            ms = df["timestamp"][e] - df["timestamp"][e - 1]

        grid[x][y] += ms  # summ-up time on cell

    ms_ges = df["timestamp"].max() - df["timestamp"].min()

    scale = 1
    grid.where(
        grid == 0,
        other=np.log10(grid * scale) / scale,
        inplace=True
    )

    print(grid.round(2))
    return grid


def drawHeatmap(arr: pandas.DataFrame):
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # cmap = sns.color_palette("blend:#7AB,#EDA", as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        arr, cmap=cmap, square=True, linewidths=0.0, cbar_kws={"shrink": .5}, vmin=0
    )

    ax.invert_yaxis()

    plt.show()


def main():
    Tk().withdraw()
    cache = CacheHandler("Unity", "Lukas Berghegger")

    res = int(11 * 1.5)  # 16 x 16

    # load input
    file_paths = utl.multiLoadCSV(cache["dataPath"], "select data")
    cache["dataPath"] = os.path.dirname(os.path.abspath(file_paths[0].name))

    # process input
    for p in file_paths:
        # prep data
        path = p.name
        df_san = sanitizeCSV(utl.parseCSV(path))
        df_prep = preprocessor(df_san, res)

        # save prep data
        basename = os.path.basename(path).split('.')[0]
        dbpath = os.path.dirname(path) + "/" + basename + "_cleaned.csv"
        df_prep.to_csv(dbpath, sep=";")

        # visualize data
        mx = calculateHeatmap(df_prep, res)
        drawHeatmap(mx)


if __name__ == "__main__":
    main()
