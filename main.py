from tkinter import Tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import pandas
import seaborn as sns

import MSSQ


def readCSV() -> pandas.DataFrame:
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


def drawHeatmap(data_in: pandas.DataFrame):
    print(data_in)

    # Load the example flights dataset and convert to long-form
    flights_long = sns.load_dataset("flights")
    flights = (flights_long.pivot(index="month", columns="year", values="passengers"))

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax)
    plt.show()


def main():
    Tk().withdraw()

    # unity_data = readCSV()
    # drawHeatmap(unity_data[["cx", "cy"]])  # find focus  # find object rest time
    MSSQ.scoreMSSQ(readCSV(), 5)


if __name__ == "__main__":
    main()
