import os

import pandas

import Utils.misc as utl
from Utils.CacheManager import CacheManager
from Utils.SQLAlchemy import SQLAlchemyHelper


def scoreSSQ(data: pandas.Series, logging: bool = False) -> pandas.Series:
    if logging:
        print(data)
        print()

    n, o, d, t = weightValues(data, logging)
    if logging:
        print("TS: " + str(t))
        print()

    return pandas.Series({"n": n, "o": o, "d": d, "ts": t}, dtype=float)


def weightValues(data: pandas.Series, logging: bool = False) -> tuple[float, float, float, float]:
    f_n = 9.54
    f_o = 7.58
    f_d = 13.92
    f_t = 3.74
    n = 0
    o = 0
    d = 0
    t = 0

    for k, v in data.items():
        match k:
            case "Generelles Unwohlsein":
                n += v
                o += v
            case "Ermüdung":
                o += v
            case "Kopfschmerzen":
                o += v
            case "Augenschmerzen":
                o += v
            case "Probleme bei der Optischen Fokussierung":
                o += v
                d += v
            case "Erhöhter Speichelfluss":
                n += v
            case "Schwitzen":
                n += v
            case "Übelkeit":
                n += v
                d += v
            case "Konzentrationsprobleme":
                n += v
                o += v
            case "Kopfdruck":
                d += v
            case "Verschwommene Sicht":
                o += v
                d += v
            case "Gleichgewichtsprobleme (bei geöffneten Augen)":
                d += v
            case "Gleichgewichtsprobleme (Bei geschlossenen Augen)":
                d += v
            case "Schwindelgefühle":
                d += v
            case "Magenbeschwerden":
                n += v
            case "Aufstoßen":
                n += v

    t = (n + o + d) * f_t
    n *= f_n
    o *= f_o
    d *= f_d

    if logging:
        print("> nausea:\t\t\t" + str(n))
        print("> oculomotor:\t\t" + str(o))
        print("> disorientation:\t" + str(d))
        print()

    return n, o, d, t


def compare_SSQ(df: pandas.DataFrame) -> pandas.DataFrame:
    out = pandas.DataFrame()
    out["Test1"] = df["post1"] - df["pre1"]
    out["Rest"] = df["pre2"] - df["post1"]
    out["Test2"] = df["post2"] - df["pre2"]
    return out


def eval_Participant(cache: CacheManager, logging: bool = False):
    # load prerequisites
    db = SQLAlchemyHelper("../test.db", True)
    ssq_path = utl.loadCachedPath(cache, "data")

    # calc paths
    src_name = os.path.basename(ssq_path).split('.')[0]
    dst_dir = os.path.dirname(ssq_path) + "/artifacts/"
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    total_path = dst_dir + src_name + "_ssq_total.csv"
    change_path = dst_dir + src_name + "_ssq_change.csv"

    # load raw values
    raw_ssq = utl.parseCSV(ssq_path)

    ssq = pandas.DataFrame()
    # iterate tests
    for t in raw_ssq:
        if logging:
            print(t + ":")
        ssq[t.strip()] = scoreSSQ(raw_ssq[t], logging)

    comp = compare_SSQ(ssq)

    # log data
    if logging:
        print("total ssq per dataset:")
        print(ssq)
        print()

    if logging:
        print("change in ssq:")
        print(comp)
        print()

    # to file
    ssq.round(3).to_csv(total_path, sep=";", decimal=",")
    comp.round(3).to_csv(change_path, sep=";", decimal=",")

    # to database



def main():
    cache = CacheManager("SSQ", "Lukas Berghegger")

    eval_Participant(cache)


if __name__ == "__main__":
    main()
