def pairs_from_distances(full_distances, cutoff=0.3):
    pairs_under_threshold = set()
    pairs_over_threshold = set()


    for distance_entry in full_distances:
        cluster_a = distance_entry[0]
        cluster_b = distance_entry[1]
        distance = distance_entry[2]

        # pairs are only one way. check if reverse exists if you test later
        pair = (cluster_a, cluster_b)
        
        if distance < cutoff:
            pairs_under_threshold.add(pair)
        else:
            pairs_over_threshold.add(pair)

    return pairs_under_threshold, pairs_over_threshold
