from tkinter import filedialog
from tkinter import Tk

import pandas


def readCSV(path: str) -> pandas.DataFrame:
    print(path)
    print()
    out = pandas.read_csv(path, sep=";", index_col=0)
    return out


def loadCSV(defaultPath: str) ->pandas.DataFrame:


def parse_vectors(stream: pandas.Series) -> pandas.DataFrame:
    buff = {"x": {}, "y": {}}
    for k, v in stream.items():
        vect2 = v.split(",")
        buff["x"][k] = vect2[0]
        buff["y"][k] = vect2[1]
    buff = pandas.DataFrame(buff).sort_values(inplace="true")
    print(buff)

    return buff
