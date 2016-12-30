import numpy as np

def bias(predicted,reference):
    '''
    Calculate the bias (B) between two variables PREDICTED and 
    REFERENCE (E'). The latter is calculated using the formula:

    B = mean(p) - mean(r)

    where p is the predicted values, and r is the reference values.
    Note that p & r must have the same number of values.

    Input:
    PREDICTED : predicted field
    REFERENCE : reference field

    Output:
    B : bias between predicted and reference

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Dec 9, 2016
    '''

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

    # Calculate means
    b = np.mean(predicted) - np.mean(reference)

    return b
