from tkinter import Tk

import matplotlib.pyplot as plt
import pandas
import seaborn as sns

import SUS
from MSSQ import MSSQ
from Utils import Utils
from Utils.Utils import parseCSV


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
    MSSQ.scoreMSSQ(parseCSV(), 5)
    # SSQ.scoreSSQ(readCSV())
    # sus_score = SUS.scoreSUS(Utils.readCSV())
    plt.show()


if __name__ == "__main__":
    main()
