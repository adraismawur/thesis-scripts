import validation


def run(euclidean_dists, truth_pairs):
    """Performs a run of euclidean distance classficiation tests with cutoffs
    on both sides"""
    
    print("Predictions from euclidean distances (both):")
    validation.print_stats_header(["cut_low", "cut_upp"])
    # generate a set of cutoffs
    for i in range(5):
        for j in range(10):
            lower_cutoff = i * 10
            upper_cutoff = j * 100
            pred_pairs = validation.pairs_from_distances(
                euclidean_dists,
                lower_cutoff,
                upper_cutoff
            )

            validation.print_stats_row(
                [
                    str(lower_cutoff),
                    str(upper_cutoff)
                ],
                truth_pairs,
                pred_pairs
            )
