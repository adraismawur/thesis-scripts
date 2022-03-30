from sklearn.cluster import KMeans

def cluster_kmeans(features, bgc_id_name_dict, max_iter, n_clusters):
    kmeans = KMeans(n_clusters, max_iter=max_iter, copy_x=False)
    results = kmeans.fit(features)

    num_clusters = max(results.labels_)
    clusters = [[] for i in range(num_clusters + 1)]

    for bgc_id, cluster in enumerate(results.labels_):
        idx = int(bgc_id) + 1
        clusters[cluster].append(bgc_id_name_dict[idx])


    # turn predictions into pair list
    pred_under_cutoff = set()
    pred_over_cutoff = set()
    pred_unclassified = set()

    for cluster_a_idx in range(len(clusters)):
        for cluster_b_idx, cluster_b in enumerate(clusters[cluster_a_idx:]):
            for idx, bgc_a in enumerate(cluster_b):
                for bgc_b in cluster_b[idx+1:]:
                    pair = tuple(sorted((bgc_a, bgc_b)))
                    if cluster_a_idx == cluster_b_idx:
                        pred_under_cutoff.add(pair)
                    else:
                        pred_over_cutoff.add(pair)

    return pred_under_cutoff, pred_over_cutoff, pred_unclassified