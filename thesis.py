from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import data
import truth.truth as truth
import input.paths as paths
import input.bigslice_hmm
import plots.hist

import predictions
import predictions.tests

import validation


print("Loading truth")
# load truth values
TRUTH_DISTANCES = truth.from_file(paths.FULL_TSV)

# show hist of true distances
# plots.hist.from_distances(TRUTH_DISTANCES, max=len(TRUTH_DISTANCES), bins=50)

TRUTH_PAIRS = validation.pairs_from_distances(TRUTH_DISTANCES)

print("Loading stored info from database")
DB = data.Database(paths.SQLITE_DB)

BGC_IDS = data.get_bgc_ids(DB)
HMM_IDS = data.get_hmm_ids(DB)

BGC_ID_NAME_DICT = data.get_bgc_id_name_dict(DB)
BGC_NAME_ID_DICT = {name: id for id, name in BGC_ID_NAME_DICT.items()}

# get a dataframe of labels associated with each BGC based on truth
# this means a dataframe of bgcs where bgcs with a distance of < 0.3 belong to
# the same 'cluster'
TRUTH_LABELS = validation.labels_from_distances(TRUTH_DISTANCES, BGC_NAME_ID_DICT, BGC_IDS)

CORE_PFAM_ACC, CORE_PFAM_NAMES = input.bigslice_hmm.get_core_pfam(paths.CORE_PFAM_TSV)
BIO_PFAM_ACC, BIO_PFAM_NAMES = input.bigslice_hmm.get_bio_pfam(paths.BIO_PFAM_TSV)
# get corresponding ids
CORE_PFAM_IDS = data.get_core_pfam_ids(DB, CORE_PFAM_ACC, CORE_PFAM_NAMES)
BIO_PFAM_IDS = data.get_bio_pfam_ids(DB, BIO_PFAM_ACC, BIO_PFAM_NAMES)
CORE_PFAM_SET = set(CORE_PFAM_IDS)
BIO_PFAM_SET = set(BIO_PFAM_IDS)


print("Instantiating dataframes")
# instantiate dataframes
FEATURES = pd.DataFrame(
    np.zeros((len(BGC_IDS), len(HMM_IDS)), dtype=np.uint8),
    index=BGC_IDS,
    columns=HMM_IDS
)

# fetch feature values from db
BGC_HMM_FEATURES = data.get_features(DB)
for bgc_id, hmm_id, value in BGC_HMM_FEATURES:
    FEATURES.at[bgc_id, hmm_id] = value

# draw a histogram of value distribution in the features
# plt.hist(FEATURES.sample(10), density=True)
# plt.show()

# this dataframe contains sums of features from biosynthetic pfams and core pfams separately
SUMS_CORE = pd.DataFrame(FEATURES[CORE_PFAM_IDS].sum(axis=1), columns=["sum_core"])
SUMS_BIO = pd.DataFrame(FEATURES[BIO_PFAM_IDS].sum(axis=1), columns=["sum_bio"])
FEATURES_SUMS = pd.merge(SUMS_CORE, SUMS_BIO, left_index=True, right_index=True)

LABEL_LIST = [TRUTH_LABELS.at[bgc_id,"label"] for bgc_id in BGC_IDS]

# show a plot of how this data looks lke
plt.scatter(FEATURES_SUMS["sum_core"], FEATURES_SUMS["sum_bio"], c=LABEL_LIST)
plt.show()

# print("Calculating euclidean distance")
# EUCLIDEAN_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="euclidean")
# plots.hist.from_distances(EUCLIDEAN_DISTS, bins=50)

# predictions.tests.euclidean_both.run(EUCLIDEAN_DISTS, TRUTH_PAIRS)

# predictions.tests.euclidean_upper.run(EUCLIDEAN_DISTS, TRUTH_PAIRS)

# print("Calculating manhattan distance")
# MANHATTAN_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="manhattan")
# plots.hist.from_distances(MANHATTAN_DISTS, bins=50)

# print("Classification using cutoff manhattan - both upper/lower")
# predictions.tests.euclidean_both.run(MANHATTAN_DISTS, TRUTH_PAIRS)
# print("Classification using cutoff manhattan - only upper")
# predictions.tests.euclidean_upper.run(MANHATTAN_DISTS, TRUTH_PAIRS)

# print("Calculating Chebyshev distance")
# CHEBYSHEV_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="chebyshev")
# plots.hist.from_distances(CHEBYSHEV_DISTS, bins=50)

# print("Classification using cutoff chebyshev - both upper/lower")
# predictions.tests.euclidean_both.run(CHEBYSHEV_DISTS, TRUTH_PAIRS)
# print("Classification using cutoff chebyshev - only upper")
# predictions.tests.euclidean_upper.run(CHEBYSHEV_DISTS, TRUTH_PAIRS)

# print("Clustering using kmeans")
# predictions.tests.kmeans.run(FEATURES, BGC_ID_NAME_DICT, TRUTH_PAIRS)


print("Clustering using kmeans - sums data")
predictions.tests.kmeans.run(FEATURES_SUMS, BGC_ID_NAME_DICT, TRUTH_PAIRS)

# print("Clustering using birch")
# predictions.tests.birch.run(FEATURES, BGC_ID_NAME_DICT, TRUTH_PAIRS)

 
# print("Clustering using Affinity Propagation")
# predictions.tests.ap.run(FEATURES, BGC_ID_NAME_DICT, TRUTH_PAIRS)
