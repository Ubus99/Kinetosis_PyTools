import os

import pandas
from sqlalchemy.orm import Session

import Utils.misc as utl
from SSQ_Class import SSQ
from Utils.CacheManager import CacheManager
from Utils.Participant_Class import Participant
from Utils.SQLAlchemy import SQLAlchemyHelper


def scoreSSQ(data: pandas.Series, logging: bool = False) -> SSQ:
    if logging:
        print(data)
        print()

    ssq = weightValues(data, logging)
    if logging:
        print("TS: " + str(ssq.ts))
        print()

    return ssq


def weightValues(data: pandas.Series, logging: bool = False) -> SSQ:
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

    ts = (n + o + d) * f_t
    n *= f_n
    o *= f_o
    d *= f_d

    if logging:
        print("> nausea:\t\t\t" + str(n))
        print("> oculomotor:\t\t" + str(o))
        print("> disorientation:\t" + str(d))
        print()

    return SSQ(n=n, o=o, d=d, ts=ts)


def compare_SSQ(df: pandas.DataFrame) -> pandas.DataFrame:
    out = pandas.DataFrame()
    out["Test1"] = df["post1"] - df["pre1"]
    out["Rest"] = df["pre2"] - df["post1"]
    out["Test2"] = df["post2"] - df["pre2"]
    return out


def save_to_file(path: str, name: str, ssq: pandas.DataFrame, comp: pandas.DataFrame):
    dst_dir = os.path.dirname(path) + "/artifacts/"
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    total_path = dst_dir + name + "_ssq_total.csv"
    change_path = dst_dir + name + "_ssq_change.csv"

    ssq.round(3).to_csv(total_path, sep=";", decimal=",")
    comp.round(3).to_csv(change_path, sep=";", decimal=",")


def save_to_database(name: str, df: pandas.DataFrame):
    db = SQLAlchemyHelper("../test.db", True)
    with Session(db.engine) as session:
        participant = Participant.load(session, name)


def eval_Participant(cache: CacheManager, logging: bool = False):
    # load prerequisites
    ssq_path = utl.loadCachedPath(cache, "data")
    src_name = os.path.basename(ssq_path).split('.')[0]

    # load raw values
    raw_ssq = utl.parseCSV(ssq_path)

    ssq = pandas.DataFrame()
    # iterate tests
    for t in raw_ssq:
        if logging:
            print(t + ":")
        ssq[t.strip()] = scoreSSQ(raw_ssq[t], logging).Series()

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
    save_to_file(ssq_path, src_name, ssq, comp)

    # to database
    # save_to_database(src_name, ssq)


def main():
    cache = CacheManager("SSQ", "Lukas Berghegger")

    eval_Participant(cache, True)


if __name__ == "__main__":
    main()
