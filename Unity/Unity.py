import os.path
from tkinter import Tk
from typing import Any

import numpy as np
import pandas

import Eyetracking.Heatmap as ET
import Utils.misc as utl
from Utils.CacheManager import CacheManager


def sanitizeCSV(df: pandas.DataFrame, key: Any, logging: bool = False) -> pandas.DataFrame:
    print("sanitizer input:")
    print(df)
    df.columns = df.columns.str.strip()  # strip whitespace from columns todo why apply to columns not whole frame?
    df = df.replace(r"^ +| +$", r"", regex=True)  # forgot what this does :(
    df = removeDuplicates(df, key).iloc[1:]  # cull duplicates, then cut index for further processing

    out = extractValidData(df, "Mode", logging)  # todo remove hardcoding

    return out


def removeDuplicates(df: pandas.DataFrame, key: Any) -> pandas.DataFrame:
    return df.drop_duplicates(subset=key)


def extractValidData(df: pandas.DataFrame, key: Any, logging: bool = False) -> pandas.DataFrame:
    if logging:
        print("removing invalid Data from " + key)

    series = df[key]  # extract relevant series
    series.reset_index(drop=True, inplace=True)  # remove manual index for iteration
    series.apply(lambda s: str(s).strip())  # strip all whitespace
    series.where(  # set all empty fields to None for bound detection
        series != "",
        other=None,
        inplace=True
    )
    first = series.first_valid_index()  # find index where "key" first contains data
    last = series.last_valid_index()  # find index where "key" last contains data

    out = df.iloc[first:last]
    if logging:
        print(out)
    return out  # return only valid data


def preprocessor(df: pandas.DataFrame, res: int) -> pandas.DataFrame:
    print("preprocessor input:")
    print(df)

    print("loading vectors:")
    v_list = []

    for e in df.index:  # load floats into vector, replaces "," notation with "." notation
        x = float((df["GazeX"][e]).replace(",", "."))
        y = float((df["GazeY"][e]).replace(",", "."))
        v = np.array([x, y])  # stores vector as 2d numpy array
        v_list.append(v)  # append vector to list of vectors

    v_list = np.asarray(v_list)  # import list
    print(v_list)
    print()

    print("fitting vectors:")
    v_mag = np.linalg.norm(v_list, axis=1) * 2  # get magnitude of all vectors
    v_scaled = v_list / v_mag.max()  # scale such that the largest vector has magnitude 1
    v_scaled += 0.5  # change coordinates from -0.5 to + 0.5 notation to 0 to 1 notation
    print(v_scaled)
    print()

    print("scaling vectors:")
    v_scaled *= (res - 1)  # scale to fit matrix
    print(v_scaled)
    print()

    v_int = ET.coordinate_binning(v_scaled, res, True)

    print("compositing dataframe.")
    out = pandas.DataFrame(v_int, columns=["x", "y"])
    timestamp = df["tobii_timestamp"].astype(int).to_list()
    out["timestamp"] = timestamp
    print()
    return out


def main():
    Tk().withdraw()
    cache = CacheManager("Unity", "Lukas Berghegger")

    res = int(11 * 1.5)  # 16 x 16

    # load input
    file_paths = utl.multiLoadCSV(cache["dataPath"], "select data")
    cache["dataPath"] = os.path.dirname(os.path.abspath(file_paths[0].name))

    # process input
    for p in file_paths:
        # prep data
        path = p.name
        df_san = sanitizeCSV(utl.parseCSV(path), "tobii_timestamp", True)
        df_prep = preprocessor(df_san, res)

        # save prep data
        basename = os.path.basename(path).split('.')[0]
        dbpath = os.path.dirname(path) + "/" + basename + "_cleaned.csv"
        df_prep.to_csv(dbpath, sep=";")

        # visualize data
        mx = ET.calculate_heatmap(df_prep, res)
        f, ax = ET.draw_heatmap(mx)
        img_path = path.split(".")[0] + ".png"
        f.savefig(img_path)

        # plt.show()


if __name__ == "__main__":
    main()
