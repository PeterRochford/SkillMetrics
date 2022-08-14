import numpy as np

def use_sci_notation(value):
    '''
    Boolean function to determine if scientific notation to be used for value
 
    Input:
    Value : value to be tested
 
    Return:
        True if absolute value is > 100 or < 1.e-3
        False otherwise

    Author: Peter A. Rochford
        Symplectic, LLC

    Created on May 10, 2022
    '''
    if (abs(value)>0 and abs(value) < 1e-3):
        return True
    else:
        return False
