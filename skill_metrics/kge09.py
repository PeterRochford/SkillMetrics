import numpy as np

def kge09(predicted, reference, sr=1.0, salpha=1.0, sbeta=1.0):
    """
    Calculate the Kling-Gupta efficiency from 2009 paper.

    Calculates the Kling-Gupta efficiency between two variables
    predicted and reference. The kge09 is calculated using the
    formula:

    KGE09 = 1 - sqrt((cc-1)**2 + (alpha-1)**2 + (beta-1)**2)

    where:
        cc = correlation coefficient between predicted and reference;
        alpha = std(predicted) / std(reference)
        beta = sum(predicted) / sum(reference)

    where s is the predicted values, o is the reference values, and
    N is the total number of values in s & o. Note that s & o must
    have the same number of values.

    Kling-Gupta efficiency can range from -infinity to 1. An efficiency of 1 (E
    = 1) corresponds to a perfect match of model to reference data.
    Essentially, the closer the model efficiency is to 1, the more accurate the
    model is.

    The efficiency coefficient is sensitive to extreme values and might yield
    sub-optimal results when the dataset contains large outliers in it.

    Kling-Gupta efficiency can be used to quantitatively describe the accuracy
    of model outputs. This method can be used to describe the predictive
    accuracy of other models as long as there is reference data to compare the
    model results to.

    Input:
    predicted : predicted values
    reference : reference values
    sr : [optional, defaults to 1.0] scaling factor for correlation
    salpha : [optional, defaults to 1.0] scaling factor for alpha
    sbeta : [optional, defaults to 1.0] scaling factor for beta

    Output:
    kge09 : Kling-Gupta Efficiency

    References:
    Gupta, Hoshin V., Harald Kling, Koray K. Yilmaz, Guillermo F. Martinez.
    Decomposition of the mean squared error and NSE performance criteria:
    Implications for improving hydrological modelling. Journal of Hydrology,
    Volume 377, Issues 1-2, 20 October 2009, Pages 80-91. DOI:
    10.1016/j.jhydrol.2009.08.003. ISSN 0022-1694
    """
    # Check that dimensions of predicted and reference fields match
    pdims= predicted.shape
    rdims= reference.shape
    if not np.array_equal(pdims,rdims):
        message = 'predicted and reference field dimensions do not' + \
            ' match.\n' + \
            'shape(predicted)= ' + str(pdims) + ', ' + \
            'shape(reference)= ' + str(rdims) + \
            '\npredicted type: ' + str(type(predicted))
        raise ValueError(message)

    for name, term in [('sr', sr), ('salpha', salpha), ('sbeta', sbeta)]:
        if term > 1 or term < 0:
            raise ValueError("'{0}' must be between 0 and 1, you gave {1}".format(name, term))

    std_ref = np.std(reference)
    if std_ref == 0:
        return -np.inf
    sum_ref = np.sum(reference)
    if sum_ref == 0:
        return -np.inf
    alpha = np.std(predicted) / std_ref
    beta = np.sum(predicted) / sum_ref
    cc = np.corrcoef(reference, predicted)[0, 1]

    # Calculate the kge09
    kge09 = 1.0 - np.sqrt((sr*(cc-1.0))**2 +
                          (salpha*(alpha-1.0))**2 +
                          (sbeta*(beta-1.0))**2)

    return kge09
