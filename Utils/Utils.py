from tkinter import filedialog
from tkinter import Tk

import pandas


def readCSV() -> pandas.DataFrame:
    Tk().withdraw()
    file_path = filedialog.askopenfile(filetypes=[("CSV", "*.csv; *.CSV")]).name
    print(file_path)

    out = pandas.read_csv(file_path, sep=";", index_col=0)
    return out


def parse_vectors(stream: pandas.Series) -> pandas.DataFrame:
    buff = {"x": {}, "y": {}}
    for k, v in stream.items():
        vect2 = v.split(",")
        buff["x"][k] = vect2[0]
        buff["y"][k] = vect2[1]
    buff = pandas.DataFrame(buff).sort_values(inplace="true")
    print(buff)

    return buff
