import scipy
from sklearn.metrics.pairwise import cosine_similarity
def get_cosine_distance(features, bgc_id_name_dict):

    distances = []

    sim = cosine_similarity(features)

    for sim_1_idx, sim_1_dists in enumerate(sim):
        for sim_2_idx, distance in enumerate(sim_1_dists[sim_1_idx+1:]):
            bgc_a_id = features.index[sim_1_idx]
            bgc_b_id = features.index[sim_2_idx]
            bgc_a_name = bgc_id_name_dict[bgc_a_id]
            bgc_b_name = bgc_id_name_dict[bgc_b_id]
            distances.append((bgc_a_name, bgc_b_name, 1 - distance))

    # for idx, bgc_a_id in enumerate(features.index):
    #     for bgc_b_id in features.index[idx+1:]:
    #         sim = cosine_similarity(
    #             features.loc[bgc_a_id][features.loc[bgc_a_id] > 0],
    #             features.loc[bgc_b_id][features.loc[bgc_b_id] > 0]
    #         )
    #         bgc_a_name = bgc_id_name_dict[bgc_a_id + 1]
    #         bgc_b_name = bgc_id_name_dict[bgc_b_id + 1]
    #         distance = sim[bgc_a_id][bgc_b_id]
    #         distances.append((bgc_a_name, bgc_b_name, distance))

    return distances