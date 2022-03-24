def print_confusion_matrix(truth, predictions):
    true_pairs_under_treshold, true_pairs_over_treshold = truth
    pred_pairs_under_treshold, pred_pairs_over_treshold = predictions
    
    true_pairs_all = true_pairs_under_treshold + true_pairs_over_treshold
    pred_pairs_all = pred_pairs_under_treshold + pred_pairs_over_treshold
    missing_pairs = true_pairs_all - pred_pairs_all

    true_positive = 
    

    return