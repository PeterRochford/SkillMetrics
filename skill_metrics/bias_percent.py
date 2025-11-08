from . import utils

import numpy as np

def bias_percent(predicted,reference):
    '''
    Calculate the percentage bias (B) between two variables PREDICTED and
    REFERENCE (E'). The latter is calculated using the formula:

    BP = 100*(mean(p) - mean(r))/mean(r)

    where p is the predicted values, and r is the reference values.
    Note that p & r must have the same number of values.

    Input:
    PREDICTED : predicted field
    REFERENCE : reference field

    Output:
    B : bias between predicted and reference

    Author: Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Jun 27, 2023
    '''

    utils.check_arrays(predicted, reference)

    # Calculate means
    model = np.mean(predicted)
    ref = np.mean(reference)
    if ref != 0.0:
        bp = 100*abs((model - ref)/ref)
    else:
        bp = NaN

    return bp
