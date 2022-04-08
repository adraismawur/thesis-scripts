import multiprocessing
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
import math
import validation

def cosine_worker(
    working_q,
    output_q,
    bgc_name_id_dict,
    bgc_hmm_ids,
    bgc_hmm_values
):
    while True:
        bgc_name_a, bgc_name_b, truth_dist = working_q.get(True)
        if bgc_name_a is None:
            break

        bgc_a_id = bgc_name_id_dict[bgc_name_a]
        bgc_b_id = bgc_name_id_dict[bgc_name_b]
        
        hmm_ids_a = bgc_hmm_ids[bgc_a_id]
        hmm_ids_b = bgc_hmm_ids[bgc_b_id]

        either = hmm_ids_a | hmm_ids_b
        # assume any with overlap 0 to be totally distant
        if len(either) == 0:
            COSINE_DIST_CORR.append([bgc_a_id, bgc_b_id, 1])
            count += 1
            continue
        # start calculation
        # get values
        hmm_values_a = bgc_hmm_values[bgc_a_id]
        hmm_values_b = bgc_hmm_values[bgc_b_id]

        # get sum product
        sum_product = 0
        a_list = []
        b_list = []
        for hmm_id in either:
            if hmm_id in hmm_values_a:
                value_a = hmm_values_a[hmm_id]
            else:
                value_a = 0

            if hmm_id in hmm_values_b:
                value_b = hmm_values_b[hmm_id]
            else:
                value_b = 0
            
            sum_product += value_a * value_b
            a_list.append(value_a ** 2)
            b_list.append(value_b ** 2)

        
        # get sum squares
        sum_root_square_a = math.sqrt(sum(a_list))
        sum_root_square_b = math.sqrt(sum(b_list))

        similarity = sum_product / (sum_root_square_a * sum_root_square_b)
        distance = 1 - similarity
        output_q.put((bgc_name_a, bgc_name_b, distance))
    return


if __name__ == '__main__':
    print("Loading truth")
    # load truth values
    TRUTH_DISTANCES = truth.from_file(paths.FULL_TSV)

    # show hist of true distances
    # plots.hist.from_distances(TRUTH_DISTANCES, max=len(TRUTH_DISTANCES), bins=50)

    TRUTH_PAIRS = validation.pairs_from_distances(TRUTH_DISTANCES)

    print("Loading stored info from database")
    DB = data.Database(paths.SQLITE_DB)


    # validation.print_full_stats(
    #     TRUTH_PAIRS,
    #     TRUTH_PAIRS
    # )

    BGC_IDS = data.get_bgc_ids(DB)
    HMM_IDS = data.get_hmm_ids(DB)

    BGC_ID_NAME_DICT = data.get_bgc_id_name_dict(DB)
    BGC_NAME_ID_DICT = {name: id for id, name in BGC_ID_NAME_DICT.items()}

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
    ).replace({0: np.nan})

    # fetch feature values from db
    BGC_HMM_FEATURES = data.get_features(DB)
    for bgc_id, hmm_id, value in BGC_HMM_FEATURES:
        FEATURES.at[bgc_id, hmm_id] = value
    
    print("Done")

    print("Calculating corrected cosine distances...")

    COSINE_DIST_CORR = predictions.get_corr_cosine_dists(
        TRUTH_DISTANCES,
        BGC_HMM_FEATURES,
        BGC_IDS,
        BGC_NAME_ID_DICT,
        "average"
    )
    print("Done")

    PREDICTION_PAIRS = validation.pairs_from_distances(COSINE_DIST_CORR, None, 0.69999999)
    
    predictions.tests.distance.run_upper(
        PREDICTION_PAIRS,
        TRUTH_PAIRS,
        upper_range=8,
        upper_cutoff_start=0.3,
        upper_cutoff_step=0.1
    )

    # draw a histogram of value distribution in the features
    # plt.hist(FEATURES.sample(10), density=True)
    # plt.show()

    # this dataframe contains sums of features from biosynthetic pfams and core pfams separately
    # SUMS_CORE = pd.DataFrame(FEATURES[CORE_PFAM_IDS].sum(axis=1), columns=["sum_core"])
    # SUMS_BIO = pd.DataFrame(FEATURES[BIO_PFAM_IDS].sum(axis=1), columns=["sum_bio"])
    # FEATURES_SUMS = pd.merge(SUMS_CORE, SUMS_BIO, left_index=True, right_index=True)


    # get a dataframe of labels associated with each BGC based on truth
    # this means a dataframe of bgcs where bgcs with a distance of < 0.3 belong to
    # the same 'cluster'
    # TRUTH_LABELS = validation.labels_from_distances(TRUTH_DISTANCES, BGC_NAME_ID_DICT, BGC_IDS)

    # LABEL_LIST = [TRUTH_LABELS.at[bgc_id,"label"] for bgc_id in BGC_IDS]

    # show a plot of how this data looks lke
    # plt.scatter(FEATURES_SUMS["sum_core"], FEATURES_SUMS["sum_bio"], c=LABEL_LIST)
    # plt.show()

    # print("Calculating euclidean distance")
    # EUCLIDEAN_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="euclidean")
    # plots.hist.from_distances(EUCLIDEAN_DISTS, bins=50)

    # predictions.tests.distance.run_both(EUCLIDEAN_DISTS, TRUTH_PAIRS)

    # predictions.tests.distance.run_upper(EUCLIDEAN_DISTS, TRUTH_PAIRS)

    # print("Calculating manhattan distance")
    # MANHATTAN_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="manhattan")
    # plots.hist.from_distances(MANHATTAN_DISTS, bins=50)

    # print("Classification using cutoff manhattan - both upper/lower")
    # predictions.tests.distance.run_both(MANHATTAN_DISTS, TRUTH_PAIRS)
    # print("Classification using cutoff manhattan - only upper")
    # predictions.tests.distance.run_upper(MANHATTAN_DISTS, TRUTH_PAIRS)

    # print("Calculating Chebyshev distance")
    # CHEBYSHEV_DISTS = predictions.get_distances(FEATURES, BGC_ID_NAME_DICT, metric="chebyshev")
    # plots.hist.from_distances(CHEBYSHEV_DISTS, bins=50)

    # print("Classification using cutoff chebyshev - both upper/lower")
    # predictions.tests.distance.run_both(CHEBYSHEV_DISTS, TRUTH_PAIRS)
    # print("Classification using cutoff chebyshev - only upper")
    # predictions.tests.distance.run_upper(CHEBYSHEV_DISTS, TRUTH_PAIRS)

    # print("Calculating cosine similarity")
    # COSINE_DISTS = predictions.get_cosine_distance(FEATURES.replace({np.nan: 0}), BGC_ID_NAME_DICT)
    # predictions.tests.distance.run_both(
    #     COSINE_DISTS,
    #     TRUTH_PAIRS,
    #     lower_range=20,
    #     lower_cutoff_step = 0.05,
    #     lower_cutoff_start= 0,
    #     upper_range=1,
    #     upper_cutoff_step = 0.1,
    #     upper_cutoff_start= 1.0
    # )

    # print("Clustering using kmeans")
    # predictions.tests.kmeans.run(FEATURES, BGC_ID_NAME_DICT, TRUTH_PAIRS)


    # print("Clustering using kmeans - sums data")
    # predictions.tests.kmeans.run(FEATURES_SUMS, BGC_ID_NAME_DICT, TRUTH_PAIRS)

    # print("Clustering using birch")
    # predictions.tests.birch.run(FEATURES, BGC_ID_NAME_DICT, TRUTH_PAIRS)

    
    # print("Clustering using Affinity Propagation")
    # predictions.tests.ap.run(FEATURES, BGC_ID_NAME_DICT, TRUTH_PAIRS)
