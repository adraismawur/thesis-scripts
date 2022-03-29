def get_metrics(truth_positive, truth_negative, prediction_positive, prediction_negative):
    """Generates the tp/fp/tn/fn metrics for validation from a set of truth pairs and prediction pairs"""
    missing_positives = truth_positive - prediction_positive
    missing_negatives = truth_negative - prediction_negative

    true_positive = truth_positive & prediction_positive
    TP = len(true_positive)
    false_positive = truth_positive & prediction_negative
    FP = len(false_positive)
    true_negative = truth_negative & prediction_negative.symmetric_difference(missing_positives)
    TN = len(true_negative)
    false_negative = truth_negative & prediction_negative.symmetric_difference(missing_negatives)
    FN = len(false_negative)
    return TP, FP, TN, FN

def print_confusion_matrix(truth, predictions):
    """Prints a confusion matrix with neat statistics for validation
    
    Input:
        two lists of tuples with the same structure. each list contains a list of tuples of BGC
        pairs under the treshold or over the treshold specified earler in the program
    
    under threshold is considered a positive. over or equal to treshold is considered negative
    """
    true_pairs_under_treshold, true_pairs_over_treshold = truth
    pred_pairs_under_treshold, pred_pairs_over_treshold = predictions

    TP, FP, TN, FN = get_metrics(
        true_pairs_under_treshold,
        true_pairs_over_treshold,
        pred_pairs_under_treshold,
        pred_pairs_over_treshold
    )

    print("Total pairs in truth: ", len(truth[0]) + len(truth[1]))
    print("Total pairs in prediction: ", len(predictions[0]) + len(predictions[1]))
    print("True positives: ", TP)
    print("False positives: ", FP)
    print("True negatives: ", TN)
    print("False negatives: ", FN)
    
    precision = TP / (TP + FP)
    print("Precision: ", precision)

    sensitivity = TP / (TP + FN)
    print("Sensitivity: ", sensitivity)

    specificity = TN / (TN + FP)
    print("Specificity: ", specificity)

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    print("Accuracy: ", accuracy)

    return