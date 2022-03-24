import os
import sys


def get_distances_from_results(result_path, cutoff, bigscape_cutoff=0.3):
    full_distances = []

    # distances from network files
    lst = sorted(os.listdir(result_path))


    for file in lst:
        if file == "Network_Annotations_Full.tsv":
            continue

        network_path = os.path.join(result_path, file, f"{file}_c{cutoff}.network")

        if not os.path.exists(network_path) or not os.path.isfile(network_path):
            print(network_path, " does not exist or is not a file")
            sys.exit()

        with open(network_path) as network_file:
            # skip line
            network_file.readline()
            for line in network_file:
                lineparts = line.split("\t")
                cluster_a = lineparts[0]
                cluster_b = lineparts[1]
                distance = lineparts[2]
                full_distances.append([cluster_a, cluster_b, distance])
    return full_distances

def get_bgcs_in_bigscape(full_distances):
    bgcs_in_bigscape = set()


    for distance_entry in full_distances:
        cluster_a = distance_entry[0]
        cluster_b = distance_entry[1]
        bgcs_in_bigscape.add(cluster_a)
        bgcs_in_bigscape.add(cluster_b)

    return bgcs_in_bigscape

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

def write_full_file(path, full_distances):
    with open(path, "w", encoding="utf-8") as fullfile:
        for distance_entry in full_distances:
            fullfile.write("\t".join(distance_entry) + "\n")

def distances_from_full_file(path):
    ## distances from full file
    full_distances = []
    with open(path) as full_distances_file:
        for line in full_distances_file:
            lineparts = line.rstrip().split("\t")

            lineparts[2] = float(lineparts[2])

            full_distances.append(lineparts)
    return full_distances
