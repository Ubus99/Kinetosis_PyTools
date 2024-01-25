import os.path
from tkinter import Tk
from typing import Any

import matplotlib.pyplot as plt
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


def preprocessor_1(df: pandas.DataFrame, res: int) -> pandas.DataFrame:
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

    print("fitting vectors:")  # this means that positions are no longer comparable between captures, but spread is
    v_mag = np.linalg.norm(v_list, axis=1) * 2  # get magnitude of all vectors
    v_scaled = v_list / v_mag.max()  # scale such that the largest vector has magnitude 1
    v_scaled += 0.5  # change coordinates from -0.5 to + 0.5 notation to 0 to 1 notation
    print(v_scaled)
    print()

    print("scaling vectors:")
    v_scaled *= (res - 1)  # scale to fit matrix
    print(v_scaled)
    print()

    v_int = ET.bin_vectors(v_scaled, res, True)

    print("compositing dataframe.")
    out = pandas.DataFrame(v_int, columns=["x", "y"])
    timestamp = df["tobii_timestamp"].astype(int).to_list()
    out["timestamp"] = timestamp
    print()
    return out


def main():
    Tk().withdraw()
    cache = CacheManager("Unity", "Lukas Berghegger")

    res = int(11 * 50)  # 16 x 16

    # load input
    file_paths = utl.multiLoadCSV(cache["dataPath"], "select data")
    cache["dataPath"] = os.path.dirname(os.path.abspath(file_paths[0].name))

    # process input
    for p in file_paths:
        # enumerate paths
        src_path = p.name

        src_name = os.path.basename(src_path).split('.')[0]
        dst_dir = os.path.dirname(src_path) + "/"

        dbpath = dst_dir + src_name + "_cleaned.csv"
        img_path = dst_dir + src_name + ".png"

        # prep data
        df_san = sanitizeCSV(utl.parseCSV(src_path), "tobii_timestamp", True)
        df_pre = preprocessor_1(df_san, res)

        # save prep data
        df_pre.to_csv(dbpath, sep=";")

        # create virtual Heatmap
        hm = ET.calc_heatmap_matrix(df_pre, res, True)

        flat_x = hm.sum(0)
        dev_x = flat_x.std()
        print("vertical deviation")
        print(dev_x)

        flat_y = hm.sum(1)
        dev_y = flat_y.std()
        print("horizontal deviation")
        print(dev_y)

        # visualize Heatmap
        g = ET.draw_marginal_heatmap(hm)

        # f, ax = ET.draw_heatmap(hm)
        g.savefig(img_path)

        plt.show()


if __name__ == "__main__":
    main()
