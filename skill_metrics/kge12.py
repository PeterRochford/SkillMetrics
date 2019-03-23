import numpy as np

def kge12(predicted, reference, sr=1.0, sgamma=1.0, sbeta=1.0):
    """
    Calculate the Kling-Gupta efficiency from 2012 paper.

    Calculates the Kling-Gupta efficiency between two variables
    predicted and reference. The kge12 is calculated using the
    formula:

    kge12 = 1 - sqrt((sr*(cc-1))**2 +
                     (sgamma*(gamma-1))**2 +
                     (sbeta*(beta-1))**2
                     )

    where:
        cc = correlation coefficient between predicted and reference;
        gamma = coefficient_of_variance(predicted) /
                coefficient_of_variance(reference)
        beta = sum(predicted) / sum(reference)

    where s is the predicted values, o is the reference values, and
    N is the total number of values in s & o. Note that s & o must
    have the same number of values.

    Kling-Gupta efficiency can range from -infinity to 1. An efficiency of 1 (E
    = 1) corresponds to a perfect match of predicted to reference data.

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
    sgamma : [optional, defaults to 1.0] scaling factor for gamma
    sbeta : [optional, defaults to 1.0] scaling factor for beta

    Output:
    kge12 : Kling-Gupta Efficiency

    References:
    Kling, H., M. Fuchs, and M. Paulin (2012), Runoff conditions in the upper
    Danube basin under an ensemble of climate change scenarios. Journal of
    Hydrology, Volumes 424-425, 6 March 2012, Pages 264-277,
    DOI:10.1016/j.jhydrol.2012.01.011
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

    gamma = (np.std(predicted)/np.mean(predicted)) / (np.std(reference)/np.mean(reference))
    beta = np.sum(predicted) / np.sum(reference)
    cc = np.corrcoef(reference, predicted)[0, 1]

    # Calculate the kge12
    kge12 = 1.0 - np.sqrt((sr*(cc-1.0))**2 +
                          (sgamma*(gamma-1.0))**2 +
                          (sbeta*(beta-1.0))**2)

    return kge12
