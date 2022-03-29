import validation


def run(euclidean_dists, truth_pairs):
    """Performs a run of euclidean distance classficiation tests with cutoffs
    on only on the upper side (near BGCs)
    
    """
    
    print("Predictions from euclidean distances (lower only):")
    validation.print_stats_header(["cut_low"])
    # generate a set of cutoffs
    for i in range(10):
            lower_cutoff = i * 10
            euclid_pred = validation.pairs_from_distances(
                euclidean_dists,
                lower_cutoff,
                None
            )

            validation.print_stats_row(
                [
                    str(lower_cutoff)
                ],
                truth_pairs,
                euclid_pred
            )
