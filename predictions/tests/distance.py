import validation


def run_both(
    distances,
    truth_pairs,
    lower_range = 5,
    lower_cutoff_step = 10,
    lower_cutoff_start = 10,
    upper_range = 10,
    upper_cutoff_step = 100,
    upper_cutoff_start = 100
):
    """Performs a run of distance cutoff classficiation tests with cutoffs
    on both sides"""
    
    print("Predictions from distances (both):")
    validation.print_stats_header(["cut_low", "cut_upp"])
    # generate a set of cutoffs
    for i in range(lower_range):
        for j in range(upper_range):
            lower_cutoff = round(i * lower_cutoff_step + lower_cutoff_start, 3)
            upper_cutoff = j * upper_cutoff_step + upper_cutoff_start
            pred_pairs = validation.pairs_from_distances(
                distances,
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

def run_lower(distances, truth_pairs):
    """Performs a run of distance cutoff classficiation tests with cutoffs
    on only on the lower side (near BGCs)
    
    """
    
    print("Predictions from distances (lower only):")
    validation.print_stats_header(["cut_low"])
    # generate a set of cutoffs
    for i in range(10):
            lower_cutoff = i * 10
            euclid_pred = validation.pairs_from_distances(
                distances,
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

def run_upper(distances, truth_pairs):
    """Performs a run of distance cutoff classficiation tests with cutoffs
    on only on the upper side (distant BGCs)"""
    
    print("Predictions from distances (upper only):")
    validation.print_stats_header(["cut_upp"])
    # generate a set of cutoffs
    for i in range(20):
            upper_cutoff = i * 100
            pred_pairs = validation.pairs_from_distances(
                distances,
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

