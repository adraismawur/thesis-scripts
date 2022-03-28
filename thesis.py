import math
import os
from random import randint, seed
import sqlite3
import sys
from sklearn.cluster import Birch
from sklearn.metrics import pairwise_distances

import numpy as np
import pandas as pd

import data
import truth.truth as truth
import input.paths as paths
import input.bigslice_hmm
import plots.hist

from predictions.distances.euclidean import get_distances
# from validation.confusion import print_confusion_matrix


# load truth values
TRUTH_DISTANCES = truth.from_file(paths.FULL_TSV)

# show hist of true distances
plots.hist.from_distances(TRUTH_DISTANCES, max=len(TRUTH_DISTANCES), bins=50)


TRUTH_PAIRS = truth.pairs_from_distances(TRUTH_DISTANCES)


DB = data.Database(paths.SQLITE_DB)

BGC_IDS = data.get_bgc_ids(DB)
HMM_IDS = data.get_hmm_ids(DB)

BGC_ID_NAME_DICT = data.get_bgc_id_name_dict(DB)

CORE_PFAM_ACC, CORE_PFAM_NAMES = input.bigslice_hmm.get_core_pfam(paths.CORE_PFAM_TSV)
BIO_PFAM_ACC, BIO_PFAM_NAMES = input.bigslice_hmm.get_bio_pfam(paths.BIO_PFAM_TSV)
# get corresponding ids
CORE_PFAM_IDS = data.get_core_pfam_ids(DB, CORE_PFAM_ACC, CORE_PFAM_NAMES)
BIO_PFAM_IDS = data.get_bio_pfam_ids(DB, BIO_PFAM_ACC, BIO_PFAM_NAMES)
CORE_PFAM_SET = set(CORE_PFAM_IDS)
BIO_PFAM_SET = set(BIO_PFAM_IDS)


# instantiate arrays
FEATURES = pd.DataFrame(
    np.zeros((len(BGC_IDS), len(HMM_IDS)), dtype=np.uint8),
    index=BGC_IDS,
    columns=HMM_IDS
)

# this array contains info of which hmm is core and which is bio
FEATURES_SPLIT = pd.DataFrame(
    np.zeros((len(BGC_IDS), len(HMM_IDS) + 1), dtype=np.uint8),
    index=BGC_IDS,
    columns=HMM_IDS + ["type"]
)

# fetch feature values from db
BGC_HMM_FEATURES = data.get_features(DB)
for bgc_id, hmm_id, value in BGC_HMM_FEATURES:
    FEATURES.at[bgc_id, hmm_id] = value
    # features_split.at[bgc_id, hmm_id] = value
    # if hmm_id in core_pfam_set:
    #     features_split.at[bgc_id, "type"] = 0
    # elif hmm_id in bio_pfam_set:
        # features_split.at[bgc_id, "type"] = 1



EUCLIDEAN_DISTS = get_distances(FEATURES, BGC_ID_NAME_DICT, metric="euclidean")
plots.hist.from_distances(EUCLIDEAN_DISTS, bins=50)

MANHATTAN_DISTS = get_distances(FEATURES, BGC_ID_NAME_DICT, metric="manhattan")
plots.hist.from_distances(MANHATTAN_DISTS, bins=50)

CHEBYSHEV_DISTS = get_distances(FEATURES, BGC_ID_NAME_DICT, metric="chebyshev")
plots.hist.from_distances(CHEBYSHEV_DISTS, bins=50)

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

birch.fit(FEATURES.values)

predictions = birch.predict(FEATURES.values)
num_clusters = max(predictions)
clusters = [[] for i in range(num_clusters + 1)]

for bgc_id, cluster in enumerate(predictions):
    idx = int(bgc_id) + 1
    clusters[cluster].append(BGC_ID_NAME_DICT[idx])

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