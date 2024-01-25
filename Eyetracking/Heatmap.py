import numpy as np
import pandas
import seaborn as sns
from matplotlib import pyplot as plt


def calculate_heatmap(df: pandas.DataFrame, res: int, logging: bool = False) -> pandas.DataFrame:
    """
    takes a pandas.Dataframe in the shape [timestamp][X, Y] and sorts entries into an n*n grid weighted by time delta.\n
    X and Y must be integers from 0 to n-1

    :param df: incoming dataframe shaped [timestamp][X, Y]
    :param res: resolution of outgoing pandas.Dataframe
    :param logging: enable or disable logging
    :return: returns a pandas.DataFrame of size res * res
    """
    if logging:
        print("heatmap input:")
        print(df)

        print("init grid")
    grid = np.zeros(shape=[res, res], dtype=float)
    grid = pandas.DataFrame(grid)

    if logging:
        print("map:")

    for e in df.index:
        x = df["x"][e]
        y = df["y"][e]

        if e + 1 < len(df):  # get gaze duration
            ms = df["timestamp"][e + 1] - df["timestamp"][e]
        else:  # catch end of array
            ms = df["timestamp"][e] - df["timestamp"][e - 1]

        grid[x][y] += ms  # summ-up time on cell

    ms_ges = df["timestamp"].max() - df["timestamp"].min()  # total eyetracking duration, currently unused

    scale_matrix_log10(grid)

    if logging:
        print(grid.round(2))
    return grid


def coordinate_binning(arr: np.ndarray, res: int, logging: bool = False) -> np.ndarray:
    """
    takes a numpy array, rounds it using numpy.rint() and then clips it to 0 to res - 1 for indexing

    :param arr: numpy array of positions
    :param res: binning resolution
    :param logging: should print log
    :return: returns binned positions
    """
    if logging:
        print("binning vectors:")

    v_int = np.rint(arr).clip(0, res - 1).astype(int)

    if logging:
        print(v_int)
        print()

    return v_int


def scale_matrix_log10(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Scales a n*m DataFrame using Log10 to increase detail visibility \n
    > log(0) save
    :param df: n * m DataFrame
    :return: scaled DataFrame df
    """
    df.where(
        df == 0,
        other=np.log10(df),
        inplace=True
    )

    return df


def draw_heatmap(arr: pandas.DataFrame) -> [plt.Figure, plt.Axes]:
    """
    Creates a basic Seaborn Heatmap Based on an n*m pandas.DataFrame
    :param arr: n*m matrix of gaze durations
    :return: returns Figure and Axis of pyplot
    """
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # cmap = sns.color_palette("blend:#7AB,#EDA", as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        arr, cmap=cmap, square=True, linewidths=0.0, cbar_kws={"shrink": .5}, vmin=0
    )

    ax.invert_yaxis()

    return f, ax
