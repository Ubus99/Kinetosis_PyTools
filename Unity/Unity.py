import os.path
from tkinter import Tk
from typing import Any

import numpy as np
import pandas
from matplotlib import pyplot as plt

import Eyetracking.Heatmap as ET
import Utils.Clustering as clustering
import Utils.misc as utl
from Utils.CacheManager import CacheManager


def sanitizeCSV(df: pandas.DataFrame, key: Any, logging: bool = False) -> pandas.DataFrame:
    if logging:
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


def pack_vectors(df: pandas.DataFrame, logging: bool = False) -> pandas.DataFrame:
    if logging:
        print("packing vectors!")
        print("input:")
        print(df)

    if logging:
        print("loading vectors:")
    v_list = []

    for e in df.index:  # load floats into vector, replaces "," notation with "." notation
        x = float((df["GazeX"][e]))  # .replace(",", "."))
        y = float((df["GazeY"][e]))  # .replace(",", "."))
        v = np.array([x, y])  # stores vector as 2d numpy array
        v_list.append(v)  # append vector to list of vectors

    v_list = np.asarray(v_list)  # import list todo hack
    if logging:
        print(v_list)
        print()

    if logging:
        print("fitting vectors:")  # this means that positions are no longer comparable between captures, but spread is
    v_mag = np.linalg.norm(v_list, axis=1)  # get magnitude of all vectors
    v_fitted = v_list / v_mag.max()  # scale such that the largest vector has magnitude 1
    v_fitted /= 2  # account for values being centered around 0.5
    v_fitted += 0.5  # translate coordinates from -0.5 to + 0.5 notation to 0 to 1 notation

    if logging:
        print(v_fitted)
        print()

    if logging:
        print("compositing dataframe.")
        print()

    out = pandas.DataFrame(v_fitted, columns=["x", "y"])
    timestamp = df["tobii_timestamp"].astype(int).to_list()
    out["timestamp"] = timestamp

    return out


def scale_vectors(df: pandas.DataFrame, res: int, logging: bool = False) -> pandas.DataFrame:
    if logging:
        print("scaling vectors to fit matrix!")
        print("input:")
        print(df)

    if logging:
        print("scaling vectors:")

    v_list = df[["x", "y"]] * (res - 1)  # scale to fit matrix width

    if logging:
        print(df)
        print()

    v_int = ET.bin_vectors(v_list, res, logging)

    if logging:
        print("compositing dataframe.")
        print()

    out = pandas.DataFrame(v_int, columns=["x", "y"])
    out["timestamp"] = df["timestamp"]

    return out


def calc_std(df: pandas.DataFrame) -> pandas.Series:
    # should probably include covariance matrix
    print("deviation:")
    gaze_dev = df.std()  # calc std for x & y
    gaze_abs = np.linalg.norm(df, axis=1)  # calculate magnitude of vectors
    gaze_abs_dev = gaze_abs.std()  # calc std of magnitude

    std = gaze_dev
    std["abs_dev"] = gaze_abs_dev
    print(std.round(3))
    print()

    return std


def extract_name(path: str):
    src_name = os.path.basename(path).split('.')[0]
    name = src_name.split("_")
    return name[0] + "_" + name[1]


def generate_heatmap(df: pandas.DataFrame, res: int, out_path: str):
    img_path = out_path + ".png"
    w_img_path = out_path + "_log2.png"

    # create virtual Heatmap
    hm = ET.calc_heatmap_matrix(df, res, False)

    # visualize Heatmap
    g = ET.draw_marginal_heatmap(hm)
    g.savefig(img_path)

    ET.scale_matrix_log10(hm)
    g = ET.draw_marginal_heatmap(hm)
    g.savefig(w_img_path)


def generate_scatterplot(df: pandas.DataFrame, out_path: str, labels: list[int] = None):
    img_path = out_path + ".png"

    weight = []

    for e in df.index:
        if e + 1 < len(df):  # get gaze duration
            ms = df["timestamp"][e + 1] - df["timestamp"][e]
        else:  # catch end of array
            ms = df["timestamp"][e] - df["timestamp"][e - 1]

        weight.append(ms)

    # visualize scatterplot
    g = ET.draw_scatterplot(df, weight, labels)
    # g.savefig(img_path)

    plt.show()


def generate_deviation_data(df: pandas.DataFrame, k: int, out_path: str):
    dev = calc_std(df[["x", "y"]])

    dev["weighted"] = dev["abs_dev"] * k

    # save deviation data
    dev.round(3).to_csv(out_path, sep=";", decimal=",")

    return dev


def main():
    Tk().withdraw()
    cache = CacheManager("Unity", "Lukas Berghegger")

    res = int(11 * 5)  # 55 x 55

    # load input
    file_paths = utl.multiLoadCSV(cache["dataPath"], "select data")
    cache["dataPath"] = os.path.dirname(os.path.abspath(file_paths[0].name))

    db_path = utl.loadCSV(cache["dbPath"], "select dataBase")
    cache["dbPath"] = os.path.dirname(os.path.abspath(db_path))

    # process input
    for p in file_paths:
        # enumerate paths
        src_path = p.name

        src_name = extract_name(src_path)
        dst_dir = os.path.dirname(src_path) + "/artifacts/"
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        eval_path = dst_dir + src_name + "_eval.csv"

        # prepare data
        san_data = sanitizeCSV(utl.parseCSV(src_path), "tobii_timestamp", False)
        gaze_pos = pack_vectors(san_data)
        gaze_pos_scaled = scale_vectors(gaze_pos, res)

        # calculate k-means
        k, labels = clustering.find_opt_k(gaze_pos, 5)

        dev = generate_deviation_data(gaze_pos, k, eval_path)
        # generate_heatmap(gaze_pos_scaled, res, dst_dir + src_name)
        generate_scatterplot(gaze_pos, dst_dir + src_name, labels)

        # save DB
        try:
            db = utl.parseCSV(db_path)
        except pandas.errors.EmptyDataError:
            db = pandas.DataFrame()

        db[src_name] = dev.round(3)
        db.to_csv(db_path, sep=";", decimal=",")


if __name__ == "__main__":
    main()
