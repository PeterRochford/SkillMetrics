from . import utils

import numpy as np
from skill_metrics import brier_score

def skill_score_brier(forecast,reference,observed):
    '''

    Calculate Brier skill score (BSS) between two variables
%Calculate non-dimensional skill score (SS) between two variables using
    definition of Murphy (1988)

    Calculates the non-dimensional skill score (SS) difference between two
    probabilities FORECAST and REFERENCE relative to OBSERVED outcomes. The
    skill score is calculated using the formula:

    BSS = 1 - BS/BSref

    where BS & BSref are the Brier scores for the forecast and reference
    probability of event occurrence

    BS    = sum_(n=1)^N (f_n - o_n)^2/N
    BSref = sum_(n=1)^N (r_n - o_n)^2/N

    where f is the forecast probabilities, o is the observed probabilities
    (0 or 1), and N is the total number of values in f & o. Note that f, r,
    & o must have the same number of values.

    Input:
    FORECAST  : forecast probabilities
    REFERENCE : reference probabilities
    OBSERVED  : observed probabilities

    Output:
    BSS : Brier skill score

    Reference:
    Glenn W. Brier, 1950: Verification of forecasts expressed in terms
    of probabilities. Mon. We. Rev., 78, 1-23.

    D. S. Wilks, 1995: Statistical Methods in the Atmospheric Sciences.
    Cambridge Press. 547 pp.

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Dec 15, 2016
    '''

    utils.check_arrays(forecast, reference)

    #% Calculate skill score
    bss = 1 - brier_score(forecast,observed)/ \
          brier_score(reference,observed)
    return bss
