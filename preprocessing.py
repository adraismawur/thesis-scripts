import math
import os
from random import randint, seed
import sqlite3
import sys
from sklearn.cluster import Birch
from sklearn.metrics import pairwise_distances

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt

from data.database import Database
from data.functions import get_bgc_id_name_dict, get_bgc_ids, get_bio_pfam_ids, get_core_pfam_ids, get_features, get_hmm_ids
from data.truth import distances_from_full_file, pairs_from_distances
from input.bigslice_hmm import get_bio_pfam, get_core_pfam
from plots.hist import show_hist_plot_distances
from predictions.euclidean import get_full_dist_from_euclidean, get_pred_from_euclidean
# from validation.confusion import print_confusion_matrix

CORE_PFAM_TSV = "C:/Users/Crude/Documents/Study/Thesis/Programs/bigslice/bigslice/db/advanced/templates/corepfam.tsv"
BIO_PFAM_TSV = "C:/Users/Crude/Documents/Study/Thesis/Programs/bigslice/bigslice/db/advanced/templates/biopfam.tsv"
SQLITE_DB = "C:/Users/Crude/Documents/Source/misc/data.db"

# BIGSCAPE_CLUSTER_FILES = "/home/crude/benchmark-out/dev-100/network_files/2022-03-21_18-17-21_hybrids_global/"
FULL_TSV = "bigscape_distances.tsv"

# load truth values
bigscape_distances = distances_from_full_file(FULL_TSV)

# show hist of true distances
show_hist_plot_distances(bigscape_distances, max=len(bigscape_distances), bins=50)


truth = pairs_from_distances(bigscape_distances)


DB = Database(SQLITE_DB)

bgc_ids = get_bgc_ids(DB)
hmm_ids = get_hmm_ids(DB)

bgc_id_name_dict = get_bgc_id_name_dict(DB)

core_pfam_accessions, core_pfam_names = get_core_pfam(CORE_PFAM_TSV)
bio_pfam_accessions, bio_pfam_names = get_bio_pfam(BIO_PFAM_TSV)
# get corresponding ids
core_pfam_ids = get_core_pfam_ids(DB, core_pfam_accessions, core_pfam_names)
bio_pfam_ids = get_bio_pfam_ids(DB, bio_pfam_accessions, bio_pfam_names)
core_pfam_set = set(core_pfam_ids)
bio_pfam_set = set(bio_pfam_ids)


# instantiate arrays
features = pd.DataFrame(
    np.zeros((len(bgc_ids), len(hmm_ids)), dtype=np.uint8),
    index=bgc_ids,
    columns=hmm_ids
)

# this array contains info of which hmm is core and which is bio
features_split = pd.DataFrame(
    np.zeros((len(bgc_ids), len(hmm_ids) + 1), dtype=np.uint8),
    index=bgc_ids,
    columns=hmm_ids + ["type"]
)

# fetch feature values from db
bgc_hmm_features = get_features(DB)
count = 0
for bgc_id, hmm_id, value in bgc_hmm_features:
    count += 1
    if count % 1000 == 0:
        print(count)
    features.at[bgc_id, hmm_id] = value
    # features_split.at[bgc_id, hmm_id] = value
    # if hmm_id in core_pfam_set:
    #     features_split.at[bgc_id, "type"] = 0
    # elif hmm_id in bio_pfam_set:
        # features_split.at[bgc_id, "type"] = 1



euclidean_distances = get_full_dist_from_euclidean(features, bgc_id_name_dict, metric="euclidean")

show_hist_plot_distances(euclidean_distances, bins=50)

manhattan_distances = get_full_dist_from_euclidean(features, bgc_id_name_dict, metric="manhattan")

show_hist_plot_distances(manhattan_distances, bins=50)

seuclidean_distances = get_full_dist_from_euclidean(features, bgc_id_name_dict, metric="seuclidean")

show_hist_plot_distances(seuclidean_distances, bins=50)

# predictions = pairs_from_distances(euclidean_distances, 50)

# print_confusion_matrix(truth, predictions)


sys.exit()

# initiate birch object
birch = Birch(
    # n_clusters=None,  # no global clustering
    # compute_labels=False,  # only calc centroids
    copy=False  # data already copied
)

# set threshold
# birch.threshold = fetch_threshold(features_df, 1)
# birch.threshold = 0.1

# set flat birch
# birch.branching_factor = features_df.shape[0]

# call birch
# pp_stuff = preprocess(
#     features_df.values
# )

birch.fit(features.values)

predictions = birch.predict(features.values)
num_clusters = max(predictions)
clusters = [[] for i in range(num_clusters + 1)]

for bgc_id, cluster in enumerate(predictions):
    idx = int(bgc_id) + 1
    clusters[cluster].append(bgc_id_name_dict[idx])

# nn = NearestNeighbors(
#     metric='euclidean',
#     algorithm='brute',
#     n_jobs=1)
# nn.fit(features_df.values)

# # perform nearest neighbor search
# dists, centroids_idx = nn.kneighbors(X=features_df.values,
#                                         n_neighbors=3,
#                                             return_distance=True)

# cutoff = 50

# clusters = []
# for bgc_idx, dist_set in enumerate(dists):
#     if max(dist_set[1:]) == 0:
#         continue
#     if min(dist_set[1:]) > cutoff:
#         continue

#     # append self
#     clusters.append([bgc_id_name_dict[bgc_idx+1]])

#     for idx, dist in enumerate(dist_set[1:]):
#         if dist < cutoff:
#             clusters[-1].append(bgc_id_name_dict[centroids_idx[bgc_idx][idx]+1])

count = 0
for cluster in clusters:
    if count > 10:
        break
    if len(cluster) > 1:
        for bgc_f in cluster:
            bgc = bgc_f.split("/")[1] 
            if bgc in distance_dict:
                for candidate_f in cluster:
                    candidate = candidate_f.split("/")[1]
                    if bgc == candidate:
                        continue
                    if candidate in distance_dict[bgc]:
                        count += 1
                        print(bgc, candidate, distance_dict[bgc][candidate], len(cluster))



print("memes")
