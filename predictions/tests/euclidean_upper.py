import validation


def run(euclidean_dists, truth_pairs):
    """Performs a run of euclidean distance classficiation tests with cutoffs
    on only on the upper side (near BGCs)"""
    
    print("Predictions from euclidean distances (upper only):")
    validation.print_stats_header(["cut_upp"])
    # generate a set of cutoffs
    for i in range(20):
            upper_cutoff = i * 100
            pred_pairs = validation.pairs_from_distances(
                euclidean_dists,
                None,
                upper_cutoff
            )

            validation.print_stats_row(
                [
                    str(upper_cutoff)
                ],
                truth_pairs,
                pred_pairs
            )
