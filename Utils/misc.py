import os
from tkinter import Tk
from tkinter import filedialog

import pandas

from Utils.CacheManager import CacheManager

VALID_FILETYPES = ("CSV", "*.csv *.CSV *.txt *.TXT")


def parseCSV(path: str) -> pandas.DataFrame:
    print(path)
    print()
    out = pandas.read_csv(path, sep=";", index_col=0, decimal=",")
    return out


def multiLoadCSV(defaultPath: str, title: str) -> [str]:
    print("Loading Dataframes from filesystem\n")
    Tk().withdraw()
    file_paths = filedialog.askopenfiles(
        initialdir=defaultPath, filetypes=[VALID_FILETYPES], title=title
    )

    return file_paths


def loadCSV(defaultPath: str, title: str) -> str:
    print("Loading Dataframe from file\n")
    Tk().withdraw()
    file_path = filedialog.askopenfile(
        initialdir=defaultPath, filetypes=[VALID_FILETYPES], title=title
    ).name

    return file_path


def loadCachedPath(cache: CacheManager, name: str) -> str:
    last_path = cache[name + "Path"]
    default_path = "./"

    if last_path is not None:
        default_path = last_path
    path = loadCSV(default_path, "select " + name)

    cache[name + "Path"] = os.path.dirname(os.path.abspath(path))

    return path


def parse_vectors(stream: pandas.Series) -> pandas.DataFrame:
    buff = {"x": {}, "y": {}}
    for k, v in stream.items():
        vect2 = v.split(",")
        buff["x"][k] = vect2[0]
        buff["y"][k] = vect2[1]
    buff = pandas.DataFrame(buff).sort_values(inplace="true")
    print(buff)

    return buff


def replace_in_file(path: str, search: str, repl: str) -> None:
    file_in = open(path, "r")

    text = ""

    for l in file_in:
        line = l.strip()
        line = line.replace(search, repl)
        text += line + "\n"
    file_in.close()

    file_out = open(path, "w")
    file_out.write(text)
    file_out.close()
