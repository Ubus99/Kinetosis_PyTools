import csv
from tkinter import Tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import pandas
import seaborn as sns

Tk().withdraw()

data = {}


def readCSV():
    streams = {}
    stream_keys = []

    file_path = filedialog.askopenfile(filetypes=[("CSV", "*.csv; *.CSV")]).name
    print(file_path)

    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for idx, row in enumerate(spamreader):
            words = row[0].split(",")
            if idx == 0:
                # print(str(idx) + "> " + ", ".join(row))
                words.pop(0)
                stream_keys = words
                for name in words:
                    streams[name] = {}
            else:
                # print(str(idx) + "> " + ", ".join(row))
                tsp = words[0]
                words.pop(0)
                for idx2, value in enumerate(words):
                    streams[stream_keys[idx2]][tsp] = value

    return pandas.DataFrame.from_dict(streams)


def parse_toVectors(stream):



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
drawHeatmap()

print(data)
