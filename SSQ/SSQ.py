import os

import pandas

import Utils.Utils as utl
from Utils.Cache_Handler import CacheHandler
from WeightedValue import WeightedValue


def scoreSSQ(data: pandas.Series) -> float:
    print(data)
    print()

    n, o, p = weightValues(data)
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


def main():
    cache = CacheHandler("SSQ", "Lukas Berghegger")

    ssq_path = utl.loadCachedPath(cache, "data")
    raw_ssq = utl.parseCSV(ssq_path)

    ssq = {}
    for t in raw_ssq:
        print(t + ":")
        ssq[t.strip()] = scoreSSQ(raw_ssq[t])
    print("total ssq per dataset:")
    print(ssq)
    print()

    database_path = utl.loadCachedPath(cache, "database")

    try:
        ssq_collection = utl.parseCSV(database_path)

    except pandas.errors.EmptyDataError:
        print("file is empty")
        ssq_collection = pandas.DataFrame()

    basename = os.path.basename(ssq_path).removesuffix(".csv")
    ssq_collection[basename] = pandas.Series(ssq)
    ssq_collection.to_csv(database_path, sep=";")


if __name__ == "__main__":
    main()
