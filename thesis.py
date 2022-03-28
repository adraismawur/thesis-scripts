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

import predictions

import validation


print("Loading truth")
# load truth values
TRUTH_DISTANCES = truth.from_file(paths.FULL_TSV)

# show hist of true distances
plots.hist.from_distances(TRUTH_DISTANCES, max=len(TRUTH_DISTANCES), bins=50)


TRUTH_PAIRS = validation.pairs_from_distances(TRUTH_DISTANCES)

print("Loading stored info from database")
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


print("Instantiating dataframes")
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


print("Calculating euclidean distance")
EUCLIDEAN_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="euclidean")
plots.hist.from_distances(EUCLIDEAN_DISTS, bins=50)

# print("Calculating manhattan distance")
# MANHATTAN_DISTS = get_distances(FEATURES, BGC_ID_NAME_DICT, metric="manhattan")
# plots.hist.from_distances(MANHATTAN_DISTS, bins=50)

# print("Calculating Chebyshev distance")
# CHEBYSHEV_DISTS = get_distances(FEATURES, BGC_ID_NAME_DICT, metric="chebyshev")
# plots.hist.from_distances(CHEBYSHEV_DISTS, bins=50)

print("\n")
print("Predictions from euclidean distances:")
euclid_pred = validation.pairs_from_distances(EUCLIDEAN_DISTS, 50)

validation.print_confusion_matrix(TRUTH_PAIRS, euclid_pred)

print("\n")
print("Predictions from birch clustering:")
birch_pred = predictions.cluster_birch(FEATURES, BGC_ID_NAME_DICT, n_clusters=50, threshold=0.5, flat=False)

validation.print_confusion_matrix(TRUTH_PAIRS, birch_pred)


