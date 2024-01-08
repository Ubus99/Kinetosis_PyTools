from tkinter import Tk, filedialog
import Utils.Utils as utl

import pandas


def scoreSingleSUS(data: pandas.Series) -> dict:
    print(data)
    print()

    sus_sum = round(data.sum(), 2)
    sus_mean = round(data.mean(), 2)

    print("> SUS Count: " + str(sus_sum))
    print("> SUS Mean: " + str(sus_mean))
    print()

    return {"sum": sus_sum, "mean": sus_mean}


def scoreSUS(data: pandas.DataFrame) -> pandas.DataFrame:
    print(data)
    print()

    out = pandas.DataFrame()

    for k in data:
        out[k] = scoreSingleSUS(data[k].squeeze())

    print(out)
    print()

    return out


def importSUS():
    Tk().withdraw()
    file_path = filedialog.askopenfile(filetypes=[("CSV", "*.csv; *.CSV")]).name
    print(file_path)

    try:
        sus_collection = pandas.read_csv(file_path, sep=";", index_col=0)
    except pandas.errors.EmptyDataError:
        print("file is empty")
        sus_collection = pandas.DataFrame()

    sus = scoreSingleSUS(utl.readCSV()["value"])
    sus_collection[input("name:\n")] = sus
    sus_collection.to_csv(file_path, sep=";")


def main():
    importSUS()


if __name__ == "__main__":
    main()
