import numpy as np
import pandas
import seaborn as sns
from matplotlib import pyplot as plt


def bin_vectors(arr: np.ndarray, res: int, logging: bool = False) -> np.ndarray:
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


def calc_heatmap_matrix(df: pandas.DataFrame, res: int, logging: bool = False) -> pandas.DataFrame:
    """
    takes a pandas.Dataframe in the shape [timestamp][X, Y] and sorts entries into an n*n grid weighted by delta time.\n
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

    if logging:
        print(grid.round(2))
    return grid


def scale_matrix_log10(df: pandas.DataFrame) -> None:
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


def scale_matrix_log2(df: pandas.DataFrame) -> None:
    """
    Scales a n*m DataFrame using Log10 to increase detail visibility \n
    > log(0) save
    :param df: n * m DataFrame
    :return: scaled DataFrame df
    """
    df.where(
        df == 0,
        other=np.log2(df),
        inplace=True
    )


def matrix_lpf(df: pandas.DataFrame, cutoff: float) -> None:
    df.where(
        df > cutoff,
        other=0,
        inplace=True
    )


def draw_basic_heatmap(df: pandas.DataFrame) -> [plt.Figure, plt.Axes]:
    """
    Creates a basic Seaborn Heatmap Based on an n*m pandas.DataFrame
    :param df: n*m matrix of gaze durations
    :return: returns Figure and Axis of pyplot
    """
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # cmap = sns.color_palette("blend:#7AB,#EDA", as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        df, cmap=cmap, square=True, linewidths=0.0, cbar_kws={"shrink": .5}, vmin=0
    )

    ax.invert_yaxis()

    return f, ax


def draw_marginal_heatmap(df: pandas.DataFrame) -> sns.JointGrid:
    # partially taken from https://stackoverflow.com/a/65921757/12614118

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    g = sns.jointplot(data=df, x=0, y=1, height=9, kind='hist')
    g.ax_marg_y.cla()
    g.ax_marg_x.cla()

    sns.heatmap(
        df, cmap=cmap, square=True, linewidths=0.0, cbar=False, vmin=0, ax=g.ax_joint
    )

    g.ax_joint.tick_params(
        left=False, right=False, labelleft=False,
        labelbottom=False, bottom=False
    )

    g.ax_joint.invert_yaxis()

    y_data = df.sum(1)
    y_len = len(y_data)
    g.ax_marg_y.barh(np.arange(0.5, y_len), width=y_data)

    x_data = df.sum(0)
    x_len = len(x_data)
    g.ax_marg_x.bar(np.arange(0.5, x_len), height=x_data)

    # remove ticks between heatmao and histograms
    g.ax_marg_x.tick_params(axis='x', bottom=False, labelbottom=False)
    g.ax_marg_y.tick_params(axis='y', left=False, labelleft=False)
    # remove ticks showing the heights of the histograms
    g.ax_marg_x.tick_params(axis='y', left=False, labelleft=False)
    g.ax_marg_y.tick_params(axis='x', bottom=False, labelbottom=False)

    g.fig.subplots_adjust(hspace=0.05, wspace=0.02)  # less spaced needed when there are no tick labels

    return g


def draw_scatterplot(df: pandas.DataFrame, weight: list[float] = None, labels: list[int] = None) -> plt.axis:
    if labels is not None:
        df["cluster"] = labels

    if weight is not None:
        df["weight"] = weight

    if "cluster" in df:
        plot = sns.scatterplot(df, x="x", y="y", hue="cluster", size="weight")

    else:
        plot = sns.scatterplot(df, x="x", y="y", size="weight")

    return plot
