from bigscape_functions import fetch_threshold

def gen_bigscape_clusters(df):
    threshold = fetch_threshold(df)
    return gen_clusters(df, threshold)

def gen_default_clusters(features):
    return gen_clusters(features)

def gen_clusters(features, threshold=0.5, flat=False):
    return   
