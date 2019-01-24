def error_check_stats(predicted,reference,field=''):
    '''
    Checks the arguments provided to the statistics functions for the
    target and Taylor diagrams. THe data is provided in the predicted 
    field (PREDICTED) and the reference field (REFERENCE).
    
    If a dictionary is provided for PREDICTED or REFERENCE, then 
    the name of the field must be supplied in FIELD.
  
    The function currently supports dictionaries, lists, and np.ndarray,
    types for the PREDICTED and REFERENCE variables.
 
    Input:
    PREDICTED : predicted field
    REFERENCE : reference field
    FIELD     : name of field to use in PREDICTED and REFERENCE dictionaries
                (optional)
 
    Output:
    None.
     
    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on June 12, 2018
    
    '''
    from array import array
    import numbers
    import numpy as np
    import pandas as pd

    # Check for valid arguments
    if isinstance(predicted, dict):
        if field == '':
            raise ValueError('FIELD argument not supplied.')
        if field in predicted:
            p = predicted[field]
        else:
            raise ValueError('Field is not in PREDICTED dictionary: ' + field)
    elif isinstance(predicted, list):
        p = np.array(predicted)
    elif isinstance(predicted, np.ndarray):
        p = predicted
    elif isinstance(predicted, pd.Series):
        p = predicted.values
    else:
        raise ValueError('PREDICTED argument must be a dictionary.')
            
    if isinstance(reference, dict):
        if field == '':
            raise ValueError('FIELD argument not supplied.')
        if field in reference:
            r = reference[field]
        else:
            raise ValueError('Field is not in REFERENCE dictionary: ' + field)
    elif isinstance(reference, list):
        r = np.array(reference)
    elif isinstance(reference, np.ndarray):
        r = reference
    elif isinstance(reference, pd.Series):
        r = reference.values
    else:
        raise ValueError('REFERENCE argument must be a dictionary.')

    # Test the input fields are numeric quantities
    if isinstance(p, array):
        p = np.array(p)
    if isinstance(p, numbers.Number):
        p = np.array(p,ndmin=1)
    if not isinstance(p, np.ndarray):
        raise ValueError('Argument PREDICTED does not contain a numeric array')

    if isinstance(r, array):
        r = np.array(p)
    if isinstance(r, numbers.Number):
        r = np.array(r,ndmin=1)
    if not isinstance(r, np.ndarray):
        raise ValueError('Argument REFERENCE does not contain a numeric array')

    # Check that dimensions of predicted and reference fields match
    pshape = np.shape(p)
    rshape = np.shape(r)
    if not np.array_equal(pshape, rshape):
        raise ValueError('PREDICTED and REFERENCE fields have different shapes:\n' +
                         'shape(predicted) = ' + str(pshape) +'\n' +
                         'shape(reference) = ' + str(rshape))

    # Check that all values are finite
    if not np.isfinite(p).all():
        raise ValueError('PREDICTED field has non-finite values')
    if not np.isfinite(r).all():
        raise ValueError('REFERENCE field has non-finite values')

    return p, r