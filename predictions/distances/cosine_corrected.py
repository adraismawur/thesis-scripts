import multiprocessing
import math

from numpy import mean

def cosine_worker(
    working_q,
    output_q,
    bgc_name_id_dict,
    bgc_hmm_ids,
    bgc_hmm_values,
    imputation="zero"
):
    bgc_imputation_values = {}
    for bgc_id in bgc_hmm_values:
        if imputation == "zero":
            bgc_imputation_values[bgc_id] = 0
        if imputation == "average":
            bgc_imputation_values[bgc_id] = sum(list(bgc_hmm_values[bgc_id].values())) / len(bgc_hmm_values[bgc_id].values())

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
            output_q.put((bgc_name_a, bgc_name_b, 1))
            continue
        # start calculation
        # get values
        hmm_values_a = bgc_hmm_values[bgc_a_id]
        hmm_values_b = bgc_hmm_values[bgc_b_id]
        
        imputation_value_a = bgc_imputation_values[bgc_a_id]
        imputation_value_b = bgc_imputation_values[bgc_b_id]

        # get sum product
        sum_product = 0
        a_list = []
        b_list = []
        for hmm_id in either:
            if hmm_id in hmm_values_a:
                value_a = hmm_values_a[hmm_id]
            else:
                value_a = imputation_value_a

            if hmm_id in hmm_values_b:
                value_b = hmm_values_b[hmm_id]
            else:
                value_b = imputation_value_b
            
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

def get_corr_cosine_dists(
    truth_distances,
    bgc_hmm_features,
    bgc_ids,
    bgc_name_id_dict,
    imputation="zero"
):
    
    # set up a dict where we can quickly retrieve the relevant features for each pair of bgcs
    BGC_HMM_IDS = {}
    BGC_HMM_VALUES = {}
    for bgc_id, hmm_id, value in bgc_hmm_features:
        if bgc_id not in BGC_HMM_IDS:
            BGC_HMM_IDS[bgc_id] = set()
            BGC_HMM_VALUES[bgc_id] = {}
        BGC_HMM_IDS[bgc_id].add(hmm_id)
        BGC_HMM_VALUES[bgc_id][hmm_id] = value

    # calculate cosine distance
    cosine_dist_corr = []

    comparisons = len(truth_distances)

    num_threads = 8


    working_q = multiprocessing.Queue(num_threads)

    output_q = multiprocessing.Queue(comparisons)

    processes = []

    for thread in range(num_threads):
        thread_name = "thesis_thread_cosine_" + str(thread)
        new_process = multiprocessing.Process(
            target=cosine_worker,
            args=(
                working_q,
                output_q,
                bgc_name_id_dict,
                BGC_HMM_IDS,
                BGC_HMM_VALUES,
                imputation
            ))
        processes.append(new_process)
        new_process.start()

    index = 0
    done = 0
    while True:
        all_tasks_put = index == comparisons
        all_tasks_done = done == comparisons

        if all_tasks_put and all_tasks_done:
            break

        if not working_q.full() and not all_tasks_put:
            working_q.put(truth_distances[index])
            index += 1
            if not working_q.full():
                continue

        if not output_q.empty():
            bgc_name_a, bgc_name_b, distance = output_q.get()
            done += 1

            cosine_dist_corr.append([bgc_name_a, bgc_name_b, distance])

            bgc_a_id = bgc_name_id_dict[bgc_name_a]
            bgc_b_id = bgc_name_id_dict[bgc_name_b]

            if done % int(comparisons/10) == 0:
                print(str(round(done/comparisons * 100, 1)) + "% done")

    for thread_num in range(num_threads * 2):
        working_q.put((None, None, None))

    for process in processes:
        process.join()
        thread_name = process.name
    
    return cosine_dist_corr