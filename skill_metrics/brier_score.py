import numpy as np

def brier_score(forecast,observed):
    '''
    Calculate Brier score (BS) between two variables

    Calculates the Brier score (BS), a measure of the mean-square error of 
    probability forecasts for a dichotomous (two-category) event, such as 
    the occurrence/non-occurrence of precipitation. The score is calculated
    using the formula:

    BS = sum_(n=1)^N (f_n - o_n)^2/N
 
    where f is the forecast probabilities, o is the observed probabilities 
    (0 or 1), and N is the total number of values in f & o. Note that f & o 
    must have the same number of values, and those values must be in the 
    range [0,1].
 
    Input:
    FORECAST : forecast probabilities
    OBSERVED : observed probabilities
 
    Output:
    BS : Brier score
 
    Reference:
    Glenn W. Brier, 1950: Verification of forecasts expressed in terms 
    of probabilities. Mon. We. Rev., 78, 1-23.

    D. S. Wilks, 1995: Statistical Methods in the Atmospheric Sciences. 
    Cambridge Press. 547 pp.

    Author: Peter A. Rochford
            Acorn Science & Innovation, Inc.
            prochford@acornsi.com

    Created on Dec 15, 2016
    '''

    # Check that dimensions of forecast and observed fields match
    fdims= forecast.shape
    odims= observed.shape
    if not np.array_equal(fdims,odims):
        message = 'forecast and observed field dimensions do not' + \
            ' match.\n' + \
            'shape(forecast)= ' + str(fdims) + ', ' + \
            'shape(observed)= ' + str(odims) + \
            '\nforecast type: ' + str(type(forecast))
        raise ValueError(message)

    # Check for valid values
    index = np.where(np.logical_or(forecast < 0, forecast > 1))
    if sum(index) > 0:
        raise ValueError('Forecast has values outside interval [0,1].')
    index = np.where(np.logical_and(observed != 0, observed != 1))
    if sum(index) > 0:
        raise ValueError('Observed has values not equal to 0 or 1.')

    # Calculate score
    bs = np.sum(np.square(forecast - observed))/len(forecast)

    return bs
