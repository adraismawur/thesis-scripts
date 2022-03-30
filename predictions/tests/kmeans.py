import warnings

from sklearn.exceptions import ConvergenceWarning

import predictions
import validation


def run(features, bgc_id_name_dict, truth_pairs):
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    print("\n")
    print("Predictions from k-means clustering:")
    validation.print_stats_header(["n_clus", "max_iter"])
    
    for i in range(5, 15):
        for j in range(1,10):
            n_clusters = i
            max_iter = j * 100

            kmeans_pairs = predictions.cluster_kmeans(
                features,
                bgc_id_name_dict,
                max_iter,
                n_clusters
            )

            validation.print_stats_row([n_clusters, max_iter], truth_pairs, kmeans_pairs)
