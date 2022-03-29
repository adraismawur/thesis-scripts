import warnings

from sklearn.exceptions import ConvergenceWarning

import predictions
import validation


def run(features, bgc_id_name_dict, truth_pairs):
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    print("\n")
    print("Predictions from k-means clustering:")
    validation.print_stats_header(["n_clus"])
    
    for i in range(5, 51):
        n_clusters = i

        kmeans_pairs = predictions.cluster_kmeans(
            features,
            bgc_id_name_dict,
            n_clusters
        )

        validation.print_stats_row([n_clusters], truth_pairs, kmeans_pairs)
