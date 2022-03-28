from sklearn.neighbors import NearestNeighbors

def get_distances(features, bgc_id_name_dict, cutoff=50,
                  metric='euclidean', algorithm='auto',
                  p=2, w=1, V=1):

    no_parameters = ['euclidean', 'manhattan', 'chebyshev']
    if metric in no_parameters:
        nn = NearestNeighbors(
        metric=metric,
        algorithm=algorithm,
        n_jobs=1)
        nn.fit(features.values)
        dists, centroids_idx = nn.kneighbors(X=features.values,
                                                return_distance=True)

    full_distances = []

    for i, distances in enumerate(dists):
        # skip any that have no distances beyond itself
        if len(distances) == 1:
            continue

        # record name
        bgc_a = bgc_id_name_dict[i + 1]

        # skip first one since it is always itself

        for j, distance in enumerate(distances[1:]):
            bgc_b = bgc_id_name_dict[centroids_idx[i][j] + 1]
            full_distances.append([bgc_a, bgc_b, distance])

    return full_distances

def get_pred_from_euclidean(features, bgc_id_name_dict, cutoff=50):
    nn = NearestNeighbors(
    metric='euclidean',
    algorithm='auto',
    n_jobs=1)
    nn.fit(features.values)
    dists, centroids_idx = nn.kneighbors(X=features.values,
                                            return_distance=True)

    pred_pairs_under_cutoff = set()
    pred_pairs_over_cutoff = set()

    for i, distances in enumerate(dists):
        # skip any that have no distances beyond itself
        if len(distances) == 1:
            continue

        # record name
        bgc_a = bgc_id_name_dict[i]

        # skip first one since it is always itself

        for j, distance in distances[1:]:
            bgc_b = bgc_id_name_dict[centroids_idx[i][j]]
            if distance < cutoff:
                pred_pairs_under_cutoff.add((bgc_a, bgc_b))
            else:
                pred_pairs_over_cutoff.add((bgc_a, bgc_b))

    return pred_pairs_under_cutoff, pred_pairs_over_cutoff


    distances = []
    count = 0
    for bgc in dists:
        if len(bgc) == 1:
            continue
        for dist in bgc[1:]:
            count += 1
            distances.append(round(dist, 3))
    return