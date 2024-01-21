import pandas


def balanced_latin_squares(n: int) -> list:
    """
    Generates an n*n Dataframe filled as a latin quare \n
    numbered 0 to (n - 1) \n
    source: https://gist.github.com/graup/70b09323bfa7182fe693eecb8e749896

    :param n: size of n*n grid
    :return: n*n DataFrame
    """
    l = [[((j // 2 + 1 if j % 2 else n - j // 2) + i) % n + 1 for j in range(n)] for i in range(n)]
    if n % 2:  # Repeat reversed for odd n
        l += [seq[::-1] for seq in l]
    return l


def count_fields(df: pandas.DataFrame, cutoff: int) -> pandas.Series:
    """
    Counts the number of occurrences of each field in the first [cutoff] columns
    (mostly for debugging purposes)

    :param df: latin-square dataframe
    :param cutoff: number of columns to analyze
    :return: dataframe containing frequency of unique fields
    """
    print("analyzing number frequency:")
    buff = pandas.DataFrame()

    print(df.iloc[:, :cutoff])
    print()
    for i in range(0, cutoff):
        vc = df.iloc[:, i]
        if not buff.empty:
            buff += vc.value_counts()
        else:
            buff = vc.value_counts()

    print("result:")
    print(buff)
    print()
    return buff


def main():
    size = int(input("enter number of columns:\n"))
    grid = pandas.DataFrame(balanced_latin_squares(size))
    print(grid)
    print()
    # grid = set_num_tests(grid, 3)
    # find_cutoff_amount(grid, 2)


if __name__ == "__main__":
    main()
