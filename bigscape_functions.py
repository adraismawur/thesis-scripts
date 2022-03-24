from random import randint, seed
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances


def fetch_threshold(df: pd.DataFrame,
                    percentile: np.float,
                    num_iter: int=100,
                    num_sample: int=1000
                    ):
    seed(42)  # to make things reproducible
    if df.shape[0] < num_sample:
        num_sample = df.shape[0]
        num_iter = 1
    threshold = np.array([np.percentile(
        pairwise_distances(
            df.sample(
                num_sample,
                random_state=randint(0, 999999)
            ).values,
            metric='euclidean',
            n_jobs=-1
        ), percentile) for i in range(num_iter)]

    ).mean()
    return threshold

def preprocess(features: np.array):
    preprocessed_features = features.astype(np.float)
    preprocessed_features = preprocessed_features[
        np.argsort(np.sum(preprocessed_features, axis=1)),
        :
    ]
    return preprocessed_features
