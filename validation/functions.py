def pairs_from_distances(full_distances, lower_cutoff=0.3, upper_cutoff=0.3):
    """Generates three lists of tuples, each tuple is a pair of BGCs. The first
    list contains pairs which are under the treshold, the second list contains
    pairs over the treshold. The third list contains pairs which are neither
    over- nor under the treshold.

    pairs with a distance under the threshold are positive (related)
    pairs with a distance over the threshold are negative (unrelated)
    pairs in between thresholds are unclassified

    if either lower-cutoff or upper_cutoff is None, the following applies:
    distance >= lower_cutoff and upper_Cutoff == none: unclassified
    distance < upper_cutoff and lower_cutoff == None: unclassified

    By default this function assumes tresholds used by BiG-SCAPE, and is used
    to generate pairs from a set of BiG-SCAPE results. These tresholds are not
    appropriate for other methods of classification
    """
    if upper_cutoff is None and lower_cutoff is None:
        print("You must set either a lower or upper cutoff")
        return None, None, None

    negative = set()
    positive = set()
    unclassified = set()

    for distance_entry in full_distances:
        cluster_a = distance_entry[0]
        cluster_b = distance_entry[1]
        distance = distance_entry[2]

        # pairs are only one way. check if reverse exists if you test later
        pair = tuple(sorted((cluster_a, cluster_b)))
        
        if lower_cutoff is None:
            if distance < upper_cutoff:
                unclassified.add(pair)
            else:
                negative.add(pair)
        elif upper_cutoff is None:
            if distance < lower_cutoff:
                positive.add(pair)
            else:
                unclassified.add(pair)
        else:
            if distance < lower_cutoff:
                positive.add(pair)
            elif distance >= upper_cutoff:
                negative.add(pair)
            else:
                unclassified.add(pair)



    return positive, negative, unclassified


def check_pairs_present(truth_pairs, pred_pairs):
    all_truth = truth_pairs[0] | truth_pairs[1] | truth_pairs[2]
    all_pred = pred_pairs[0] | pred_pairs[1] | pred_pairs[2]
    
    return len(all_pred.difference(all_truth)) == 0
