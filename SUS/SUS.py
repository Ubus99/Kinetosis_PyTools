import pandas


def scoreSingleSUS(data: pandas.Series) -> tuple[float, float]:
    print(data)
    print()

    sus_sum = round(data.sum(), 2)
    sus_mean = round(data.mean(), 2)

    print("> SUS Count: " + str(sus_sum))
    print("> SUS Mean: " + str(sus_mean))
    print()

    return sus_sum, sus_mean


def scoreSUS(data: pandas.DataFrame) -> pandas.DataFrame:
    print(data)
    print()

    out = {}

    for k in data:
        buff = scoreSingleSUS(data[k].squeeze())
        out[k] = {"sus_sum": buff[0], "sus_mean": buff[1]}

    out = pandas.DataFrame(out)
    print(out)
    print()

    return out
