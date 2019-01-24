import numpy as np

def check_taylor_stats(STDs, CRMSDs, CORs, threshold = 0.01):
    '''
    Checks input statistics satisfy Taylor diagram relation to <1%.

    Function terminates with an error if not satisfied. The threshold is
    the ratio of the difference between the statistical metrics and the
    centered root mean square difference:

     abs(CRMSDs^2 - (STDs^2 + STDs(1)^2 - 2*STDs*STDs(1)*CORs))/CRMSDs^2

    Note that the first element of the statistics vectors must contain
    the value for the reference field.

    INPUTS:
    STDs      : Standard deviations
    CRMSDs    : Centered Root Mean Square Difference 
    CORs      : Correlation
    threshold : limit for acceptance, e.g. 0.1 for 10% (default 0.01)

    OUTPUTS:
    None.

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Dec 3, 2016
    '''
    if threshold < 1e-7:
        raise ValueError('threshold value must be positive: ' + str(threshold))

    diff = np.square(CRMSDs[1:]) \
           - (np.square(STDs[1:]) + np.square(STDs[0]) \
           - 2.0*STDs[0]*np.multiply(STDs[1:],CORs[1:]))
    diff = np.abs(np.divide(diff,np.square(CRMSDs[1:])))
    index = np.where(diff > threshold)
    if not index:
        ii = np.where(diff != 0)
        if len(ii) == len(diff):
            raise ValueError('Incompatible data\nYou must have:' +
                '\nCRMSDs - sqrt(STDs.^2 + STDs[0]^2 - ' +
                '2*STDs*STDs[0].*CORs) = 0 !')
        else:
            raise ValueError('Incompatible data indices: {}'.format(ii) +
                       '\nYou must have:\nCRMSDs - sqrt(STDs.^2 + STDs[0]^2 - ' +
                       '2*STDs*STDs[0].*CORs) = 0 !')

    return diff
