def get_metrics(truth_positive, truth_negative, prediction_positive, prediction_negative):
    """Generates the tp/fp/tn/fn metrics for validation from a set of truth pairs and prediction pairs"""
    missing_positives = truth_positive - prediction_positive
    missing_negatives = truth_negative - prediction_negative

    true_positive = truth_positive & prediction_positive
    TP = len(true_positive)
    false_positive = truth_negative & prediction_positive
    FP = len(false_positive)
    true_negative = truth_negative & prediction_negative
    TN = len(true_negative)
    false_negative = truth_positive & prediction_negative
    FN = len(false_negative)
    return TP, FP, TN, FN

def print_full_stats(truth, predictions):
    """Prints a confusion matrix with neat statistics for validation
    
    Input:
        truth: three lists of tuples (pairs) containing under, over and unclassified pairs
        predictions: as in truth, but for the predictions
    
    under threshold is considered a positive. over or equal to treshold is considered negative
    """
    truth_positive, truth_negative, truth_unclassified = truth
    pred_positive, pred_negative, pred_unclassified = predictions

    TP, FP, TN, FN = get_metrics(
        truth_positive,
        truth_negative,
        pred_positive,
        pred_negative
    )

    print("Total pairs in truth: ", len(truth_positive) + len(truth_negative) + len(truth_unclassified))
    print("Composition (T/F/U): ", len(truth_positive), len(truth_negative), len(truth_unclassified))
    print("Total pairs in prediction: ", len(pred_positive) + len(pred_negative) + len(pred_unclassified))
    print("Composition (T/F/U): ", len(pred_positive), len(pred_negative), len(pred_unclassified))
    print("True positives: ", TP)
    print("False positives: ", FP)
    print("True negatives: ", TN)
    print("False negatives: ", FN)
    
    if TP + FP > 0:
        precision = TP / (TP + FP)
    else:
        precision = 0.0
    print("Precision: ", precision)

    if TP + FN > 0:
        sensitivity = TP / (TP + FN)
    else:
        sensitivity = 0.0
    print("Sensitivity: ", sensitivity)

    if TN + FP > 0:
        specificity = TN / (TN + FP)
    else:
        specificity = 0.0
    print("Specificity: ", specificity)

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    print("Accuracy: ", accuracy)

    return

def print_stats_header(param_names):
    header = param_names + [
        "under",
        "over",
        "unclass",
        "prec",
        "sens",
        "spec",
        "acc",
        "ppv",
        "npv",
        "tp",
        "fp",
        "tn",
        "fn"
    ]
    print(",".join(header))

def get_stats_row(params, truth, predictions):
    truth_positive, truth_negative, truth_unclassified = truth
    pred_positive, pred_negative, pred_unclassified = predictions
    TP, FP, TN, FN = get_metrics(
        truth_positive,
        truth_negative,
        pred_positive,
        pred_negative
    )
    
    if TP + FP > 0:
        precision = str(round(TP / (TP + FP), 3))
    else:
        precision = "NA"

    if TP + FN > 0:
        sensitivity = str(round(TP / (TP + FN), 3))
    else:
        sensitivity = "NA"

    if TN + FP > 0:
        specificity = str(round(TN / (TN + FP), 3))
    else:
        specificity = "NA"

    if TP + TN + FP + FN > 0:
        accuracy = str(round((TP + TN) / (TP + TN + FP + FN), 3))
    else:
        accuracy = "NA"
    
    if TP + FP > 0:
        ppv = str(round(TP / (TP + FP), 3))
    else:
        ppv = "NA"

    if TN + FN > 0:
        npv = str(round(TN / (TN + FN), 3))
    else:
        npv = "NA"

    params = list(map(str, params))
    row = params + [
        str(len(predictions[0])),
        str(len(predictions[1])),
        str(len(predictions[2])),
        precision,
        sensitivity,
        specificity,
        accuracy,
        ppv,
        npv,
        str(TP),
        str(FP),
        str(TN),
        str(FN)
    ]
    return row

def print_stats_row(params, truth, predictions):
    row = get_stats_row(params, truth, predictions)
    print(",".join(row))
