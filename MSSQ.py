from typing import Tuple

import pandas


def scoreMSSQ(data: pandas.DataFrame, cutoff: int) -> tuple[bool, float]:
    print(data)

    print("Kind:")
    buff = scoreMSSQPart(data["Kind"], cutoff)
    mssq = buff[1]
    valid = buff[0]

    print("Erwachsen:")
    buff = scoreMSSQPart(data["Erwachsen"], cutoff)
    mssq += buff[1]
    valid |= buff[0]

    print("Total: " + str(valid) + ", " + str(mssq))
    return valid, mssq


def scoreMSSQPart(data: pandas.Series, cutoff: int) -> tuple[bool, float]:
    dl = len(data.index)
    t = 0  # not applicable
    ss = 0  # Sickness Score

    for d in data:
        if d == "t":
            t += 1
        else:
            ss += int(d)

    msx = (ss * dl) / (dl - t)
    val = t < cutoff
    print(">    NA: " + str(t))
    print(">    SS: " + str(ss))
    print(">   MSx: " + str(ss))
    print("> Valid: " + str(val))

    return val, msx
