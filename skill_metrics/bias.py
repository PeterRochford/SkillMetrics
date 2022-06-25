from . import utils

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

    utils.check_arrays(predicted, reference)

    # Calculate means
    b = np.mean(predicted) - np.mean(reference)

    return b
