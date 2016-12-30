def check_on_off(value):
    '''
    Check whether variable contains a value of 'on', 'off', True, or False.
    Returns an error if neither for the first two, and sets True to 'on',
    and False to 'off'. The 'on' and 'off' can be provided in any combination
    of upper and lower case letters.
    
    INPUTS:
    value : string or boolean to check
    
    OUTPUTS:
    None.

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''

    if isinstance(value, basestring):
        lowcase = value.lower()
        if lowcase == 'off': return lowcase
        elif lowcase == 'on': return lowcase
        else:
            raise ValueError('Invalid value: ' + str(value))
    elif isinstance(value, bool):
        if value == False: value = 'off'
        elif value == True: value = 'on'
    else:
        raise ValueError('Invalid value: ' + str(value))

    return value
