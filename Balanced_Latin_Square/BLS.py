import pandas


def balanced_latin_squares(n):
    l = [[((j // 2 + 1 if j % 2 else n - j // 2) + i) % n + 1 for j in range(n)] for i in range(n)]
    if n % 2:  # Repeat reversed for odd n
        l += [seq[::-1] for seq in l]
    return l


def set_num_tests(df: pandas.DataFrame, num: int):
    print("setting number of different Tests:")
    buff = (df % num) + 1
    print(buff)
    print()
    return buff


def find_cutoff_amount(df: pandas.DataFrame, cutoff: int) -> pandas.Series:
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
