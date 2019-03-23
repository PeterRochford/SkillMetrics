from . import utils

import numpy as np
from skill_metrics import rmsd

def skill_score_murphy(predicted,reference):
    '''
    Calculate non-dimensional skill score (SS) between two variables using
    definition of Murphy (1988)

    Calculates the non-dimensional skill score (SS) difference between two
    variables PREDICTED and REFERENCE. The skill score is calculated using
    the formula:

    SS = 1 - RMSE^2/SDEV^2

    where RMSE is the root-mean-squre error between the predicted and
    reference values

    (RMSE)^2 = sum_(n=1)^N (p_n - r_n)^2/N

    and SDEV is the standard deviation of the reference values

    SDEV^2 = sum_(n=1)^N [r_n - mean(r)]^2/(N-1)

    where p is the predicted values, r is the reference values, and
    N is the total number of values in p & r. Note that p & r must
    have the same number of values.

    Input:
    PREDICTED : predicted field
    REFERENCE : reference field

    Output:
    SS : skill score

    Reference:
    Allan H. Murphy, 1988: Skill Scores Based on the Mean Square Error
    and Their Relationships to the Correlation Coefficient. Mon. Wea.
    Rev., 116, 2417-2424.
    doi: http//dx.doi.org/10.1175/1520-0493(1988)<2417:SSBOTM>2.0.CO;2

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Dec 7, 2016
    '''

    utils.check_arrays(predicted, reference)

    # Calculate RMSE
    rmse2 = rmsd(predicted,reference)**2

    # Calculate standard deviation
    sdev2 = np.std(reference,ddof=1)**2

    #% Calculate skill score
    ss = 1 - rmse2/sdev2

    return ss
