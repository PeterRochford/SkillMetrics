def get_from_dict_or_default(options: dict, default_key: str, dict_key: str, key_key: str):
    '''
    Gets values of keys from dictionary or returns defaults.

    Given a dictionary, the key of the default value (default_key), the key of a potential
    internal dictionary (dict_key) and the key of a potential value within dict_key
    (key_key), return the value of key_key if possible, or the value of default_key
    otherwise.

    INPUTS:
    options:     Dictionary containing 'default_key' and possibly 'dict_key.key_key'
    default_key: Key of the default value within 'options'
    dict_key:    Key of the potential internal dictionary within 'options'
    key_key:     Key of the potential value within 'dict_key'

    OUTPUTS:
    return: The value of 'options.dict_key.key_key' or of 'options.default_key'

    Author: Andre D. L. Zanchetta
        adlzanchetta@gmail.com

    Created on Aug 14, 2022
    '''

    if options[dict_key] is None:
        return options[default_key]
    elif key_key not in options[dict_key]:
        return options[default_key]
    elif options[dict_key][key_key] is None:
        return options[default_key]
    else:
        return options[dict_key][key_key]
