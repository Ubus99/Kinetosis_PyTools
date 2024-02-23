import pandas
from kneed import KneeLocator
from sklearn.cluster import KMeans


def eval_elbow(sse: list[float]) -> int:
    x = range(1, len(sse) + 1)

    kl = KneeLocator(
        x, sse, curve="convex", direction="decreasing"
    )
    return kl.elbow


def find_opt_k(s: pandas.DataFrame, max_k: int) -> [int, list[int]]:
    sse = []
    labels = []
    weight = []

    for e in s.index:
        if e + 1 < len(s):  # get gaze duration
            ms = s["timestamp"][e + 1] - s["timestamp"][e]
        else:  # catch end of array
            ms = s["timestamp"][e] - s["timestamp"][e - 1]

        weight.append(ms)

    for k in range(1, max_k + 1):
        print("evaluating k=" + str(k))

        km = KMeans(k)
        km = km.fit(s[["x", "y"]], sample_weight=weight)

        sse.append(km.inertia_)
        labels.append(km.labels_)

    opt_k = eval_elbow(sse)

    if opt_k is None:
        opt_k = 1
    print("\nopt_k=" + str(opt_k) + "\n")

    """
    [[plt.style.use("fivethirtyeight")
    plt.plot(range(1, max_k + 1), sse)
    plt.xticks(range(1, max_k + 1))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()
    """

    return opt_k, labels[opt_k - 1]
