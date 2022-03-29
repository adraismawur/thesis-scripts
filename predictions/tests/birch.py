import warnings

from sklearn.exceptions import ConvergenceWarning

import predictions
import validation


def run(features, bgc_id_name_dict, truth_pairs):
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    print("\n")
    print("Predictions from birch clustering:")
    validation.print_stats_header(["n_clusters", "threshold"])
    
    for i in range(1, 10):
        for j in range(1,10):
            n_clusters = i * 10
            threshold = round(j * 0.1, 3)

            birch_pairs = predictions.cluster_birch(
                features,
                bgc_id_name_dict,
                n_clusters,
                True,
                threshold,
                False
            )

            validation.print_stats_row([str(n_clusters), str(threshold)], truth_pairs, birch_pairs)