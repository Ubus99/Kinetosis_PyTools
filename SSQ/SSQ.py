from tkinter import Tk, filedialog
import Utils.Utils as utl

import pandas


class WeightedValue:
    val = 0
    weight = 1

    def __init__(self, weight):
        self.weight = weight

    def add(self, inp: int):
        self.val += inp * self.weight


def scoreSSQ(data: pandas.DataFrame) -> float:
    print(data)
    print()

    n, o, p = weightValues(data["value"])
    out = (n + o + p) * 3.74
    print("SSQ: " + str(out))
    print()

    return round(out, 2)


def weightValues(data: pandas.Series) -> tuple[float, float, float]:
    n = WeightedValue(9.54)
    o = WeightedValue(7.58)
    d = WeightedValue(13.92)

    for k, v in data.items():
        match k:
            case "Generelles Unwohlsein":
                n.add(v)
                o.add(v)
            case "Ermüdung":
                o.add(v)
            case "Kopfschmerzen":
                o.add(v)
            case "Augenschmerzen":
                o.add(v)
            case "Probleme bei der Optischen Fokussierung":
                o.add(v)
                d.add(v)
            case "Erhöhter Speichelfluss":
                n.add(v)
            case "Schwitzen":
                n.add(v)
            case "Übelkeit":
                n.add(v)
                d.add(v)
            case "Konzentrationsprobleme":
                n.add(v)
                o.add(v)
            case "Kopfdruck":
                d.add(v)
            case "Verschwommene Sicht":
                o.add(v)
                d.add(v)
            case "Gleichgewichtsprobleme (bei geöffneten Augen)":
                d.add(v)
            case "Gleichgewichtsprobleme (Bei geschlossenen Augen)":
                d.add(v)
            case "Schwindelgefühle":
                d.add(v)
            case "Magenbeschwerden":
                n.add(v)
            case "Aufstoßen":
                n.add(v)

    print("> n: " + str(n.val))
    print("> o: " + str(o.val))
    print("> d: " + str(d.val))
    print()

    return n.val, o.val, d.val


def importSSQ():
    Tk().withdraw()
    file_path = filedialog.askopenfile(filetypes=[("CSV", "*.csv; *.CSV")]).name
    print(file_path)

    try:
        ssq_collection = pandas.read_csv(file_path, sep=";", index_col=0)
    except pandas.errors.EmptyDataError:
        print("file is empty")
        ssq_collection = pandas.DataFrame()

    ssq = scoreSSQ(utl.readCSV())
    ssq_collection[input("name:\n")] = {"ssq": ssq}
    ssq_collection.to_csv(file_path, sep=";")


def main():
    importSSQ()


if __name__ == "__main__":
    main()
