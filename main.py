from tkinter import Tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import pandas
import seaborn as sns

Tk().withdraw()

data = {}


def readCSV() -> pandas.DataFrame:
    file_path = filedialog.askopenfile(filetypes=[("CSV", "*.csv; *.CSV")]).name
    print(file_path)

    return pandas.read_csv(file_path, index_col=0)


def parse_vectors(stream: pandas.Series):
    buff = {"x": {}, "y": {}}
    for k, v in stream.items():
        vect2 = v.split(",")
        buff["x"][k] = vect2[0]
        buff["y"][k] = vect2[1]
    buff = pandas.DataFrame(buff)
    print(buff)

    return buff


def drawHeatmap():
    # Load the example flights dataset and convert to long-form
    flights_long = sns.load_dataset("flights")
    flights = (
        flights_long
        .pivot(index="month", columns="year", values="passengers")
    )

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax)
    plt.show()


data = readCSV()
parse_vectors(data["A"])
# drawHeatmap()

print(data)
