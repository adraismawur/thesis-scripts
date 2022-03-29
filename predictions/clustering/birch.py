from sklearn.cluster import Birch
from bigscape_functions import fetch_threshold

def cluster_birch(features, bgc_id_name_dict, n_clusters=None, compute_labels=False, threshold=None, flat=True):
    """Generates clusters using birch. By default this copies the method used in bigslice"""
    # initiate birch object
    birch = Birch(
        # n_clusters=None,  # no global clustering
        # compute_labels=False,  # only calc centroids
        copy=False  # data already copied
    )

    # get threshold
    if not threshold:
        threshold = fetch_threshold(features, 1)

    # set threshold
    birch.threshold = threshold

    # set flat birch
    if flat:
        birch.branching_factor = features.shape[0]

    # call birch
    # pp_stuff = preprocess(
    #     features_df.values
    # )

    birch.fit(features.values)

    predictions = birch.predict(features.values)

    num_clusters = max(predictions)
    clusters = [[] for i in range(num_clusters + 1)]

    for bgc_id, cluster in enumerate(predictions):
        idx = int(bgc_id) + 1
        clusters[cluster].append(bgc_id_name_dict[idx])


    # turn predictions into pair list
    pred_under_cutoff = set()
    pred_over_cutoff = set()
    for cluster in clusters:
        for idx, bgc_a in enumerate(cluster):
            for bgc_b in cluster[idx+1:]:
                pred_under_cutoff.add((bgc_a, bgc_b))
    return pred_under_cutoff, pred_over_cutoff
