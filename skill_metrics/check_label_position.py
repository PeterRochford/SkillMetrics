def check_label_position(value):
    '''
    Check for valid values of axis label position of 'inside', or 'outside'.
    Returns an error if none of these choices. The 'outside' and 'inside' can be 
    provided in any combination of upper and lower case letters.
    
    INPUTS:
    value : string to check
    
    OUTPUTS:
    None.

    Author: Peter A. Rochford
        rochford.peter1@gmail.com
    '''

    if isinstance(value, str):
        lowcase = value.lower()
        if lowcase == 'inside': return lowcase
        elif lowcase == 'outside': return lowcase
        else:
            raise ValueError('Invalid value: ' + str(value))
    else:
        raise ValueError('Invalid value: ' + str(value))

    return value
