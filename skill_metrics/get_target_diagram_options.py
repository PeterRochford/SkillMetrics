from skill_metrics import check_on_off
from typing import Union
import os
import pandas as pd
import re

def _check_dict_with_keys(variable_name: str, dict_obj: Union[dict, None],
                          accepted_keys: set, or_none: bool = False) -> None:
    """
    Check if an argument in the form of dictionary has valid keys.
    :return: None. Raise 'ValueError' if evaluated variable is considered invalid. 
    """
    
    # if variable is None, check if it can be None
    if dict_obj is None:
        if or_none:
            return None
        else:
            raise ValueError('%s cannot be None!' % variable_name)
    
    # check if every key provided is valid
    for key in dict_obj.keys():
        if key not in accepted_keys:
            raise ValueError('Unrecognized option of %s: %s' % (variable_name, key))
        del key
    
    return None

def _circle_color_style(option : dict) -> dict:
    '''
    Set color and style of grid circles from option['circlecolor'] and
	option['circlestyle'] 
    '''
    # decipher into color and style components
    if option['circlelinespec'][-1].isalpha():
        option['circlecolor'] = option['circlelinespec'][-1]
        option['circlestyle'] = option['circlelinespec'][0:-1]
    else:
        option['circlecolor'] = option['circlelinespec'][0]
        option['circlestyle'] = option['circlelinespec'][1:]
    
    return option

def is_int(element):
    '''
    Check if variable is an integer. 
    '''
    try:
        int(element)
        return True
    except ValueError:
        return False

def is_float(element):
    '''
    Check if variable is a float. 
    '''
    try:
        float(element)
        return True
    except ValueError:
        return False
    
def is_list_in_string(element):
    '''
    Check if variable is list provided as string 
    '''
    return bool(re.search(r'\[|\]', element))

def _default_options() -> dict:
    '''
    Set default optional arguments for target_diagram function.
    
    Sets the default optional arguments for the TARGET_DIAGRAM 
    function in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. 
    
    INPUTS:
    None
        
    OUTPUTS:
    option : dictionary containing option values
    option : dictionary containing option values. (Refer to 
             display_target_diagram_options function for more information.)
    option['alpha']           : blending of symbol face color (0.0 
                                transparent through 1.0 opaque). (Default : 1.0)
    option['axismax']         : maximum for the Bias & uRMSD axis
    option['circlecolor']     : circle line color specification (default None)
    option['circlecols']      : dictionary with two possible colors keys ('ticks',
                                'tick_labels') or None, if None then considers only the
                                value of 'circlecolor' (Default: None)
    option['circlelinespec']  : circle line specification (default dashed 
                                black, '--k')
    option['circlelinewidth'] : circle line width specification (default 0.5)
    option['circles']         : radii of circles to draw to indicate 
                                isopleths of standard deviation (empty by default)
    option['circlestyle']     : line style for circles (Default: None)

    option['cmap']            : Choice of colormap. (Default : 'jet')
    option['cmap_vmin']       : minimum range of colormap (Default : None)
    option['cmap_vmax']       : maximum range of colormap (Default : None)
    option['cmap_marker']     : marker to use with colormap (Default : 'd')
    option['cmapzdata']       : data values to use for color mapping of
                                markers, e.g. RMSD or BIAS. (Default empty)
    option['colframe']        : color for the y (left) and x (bottom) spines

    option['colormap']        : 'on'/'off' switch to map color shading of
                                 markers to CMapZData values ('on') or min to
                                 max range of CMapZData values ('off').
                                 (Default : 'on')

    option['default_colors']  : default list of marker symbols (Default: None). See function
                                get_default_markers.
    option['default_markers'] : default list of marker colors (Default: None). See function
                                get_default_markers.

    option['equalAxes']       : 'on'/'off' switch to set axes to be equal 
                                (Default 'on')
                                
    option['labelweight']     : weight of the x & y axis labels
    option['locationcolorbar'] : location for the colorbar, 'NorthOutside' or
                                 'EastOutside'
    option['markercolor']     : single color to use for all markers (Default: None)
    option['markercolors']    : dictionary with two colors as keys ('face', 'edge')
                                or None. If None or 'markerlegend' == 'on' then
                                considers only the value of 'markercolor'. (Default: None)
    option['markerdisplayed'] : markers to use for individual experiments
    option['markerlabel']     : name of the experiment to use for marker
    option['markerlabelcolor']: marker label color (Default: 'k')
    option['markerlayout']    : matrix layout for markers in legend [nrow, ncol] 
                                (Default [15, no. markers/15] ) 
    option['markerlegend']    : 'on'/'off' switch to display marker legend
                                (Default 'off')
    option['markers']         : Dictionary providing individual control of the marker
                                key - text label for marker, e.g. '14197'
                                key['labelColor'] - color of marker label, e.g. 'r' for red
                                key['symbol'] - marker symbol, e.g. 's' for square
                                key['size'] - marker size, e.g. 9
                                key['faceColor'] - marker face color, e.g. 'b' for blue
                                key['edgeColor'] - marker edge color, e.g. 'k' for black line
                                (Default: None)
    option['markersize']      : marker size (Default 10)
    option['markersymbol']    : marker symbol (Default 'o')

    option['normalized']      : statistics supplied are normalized with 
                                respect to the standard deviation of reference
                                values (Default 'off')
    option['obsUncertainty']  : Observational Uncertainty (default of 0)
    option['overlay']         : 'on'/'off' switch to overlay current
                                statistics on target diagram (Default 'off').
                                Only markers will be displayed.
    option['stylebias']       : line style for bias grid lines (Default: solid line '-')

    option['target_options_file'] : name of CSV file containing values for optional
                                arguments of the target_diagram function. If no file
                                suffix is given, a ".csv" is assumed. (Default: empty string '')

    option['ticks']           : define tick positions (default is that used 
                                by the axis function)
    option['titlecolorbar']   : title for the colorbar
    option['xticklabelpos']   : position of the tick labels along the x-axis 
                                (empty by default)
    option['yticklabelpos']   : position of the tick labels along the y-axis 
                                (empty by default)
  
    Author: Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Sep 17, 2022
    Revised on Sep 17, 2022
    '''
    from matplotlib import rcParams

    # Set default parameters for all options
    option = {}
    option['alpha'] = 1.0
    option['axismax'] = 0.0
    option['circlecols'] = None   # if None, considers 'colstd' only
    option['circlelinespec'] = 'k--'
    option['circlelinewidth'] = rcParams.get('lines.linewidth')
    option['circles'] = None
    option['circlestyle'] = None # circlelinespec by default

    option['circlecolor'] = option['circlelinespec'][0]
    option['circlestyle'] = option['circlelinespec'][1:]

    option['cmap'] = 'jet'
    option['cmap_vmin'] = None
    option['cmap_vmax'] = None
    option['cmap_marker'] = 'd'
    option['cmapzdata'] = []

    option['colframe'] = '#000000' # black
    option['colormap'] = 'on'

    option['default_colors'] = None
    option['default_markers'] = None

    option['equalaxes'] = 'on'
    
    option['labelweight'] = 'bold' # weight of the x/y labels ('light', 'normal', 'bold', ...)
    option['locationcolorbar'] = 'NorthOutside'

    option['markercolor'] = None
    option['markercolors'] = None  # if None, considers 'markercolor' only
    option['markerdisplayed'] = 'marker'
    option['markerlabel'] = ''
    option['markerlabelcolor'] = 'k'
    option['markerlayout'] = [15, None]
    option['markerlegend'] = 'off'
    option['markerobs'] = 'none'
    option['markers'] = None
    option['markersize'] = 10
    option['markersymbol'] = 'o'

    option['normalized'] = 'off'
    option['obsuncertainty'] = 0.0
    option['overlay'] = 'off'
    
    option['stylebias'] = '-.'
        
    option['target_options_file'] = ''
    
    option['ticks'] = []
    option['titlecolorbar'] = ''
    option['xticklabelpos'] = []
    option['yticklabelpos'] = []
                       
    return option

def _get_options(option, **kwargs) -> dict:
    '''
    Get values for optional arguments for target_diagram function.
    
    Gets the default optional arguments for the TARGET_DIAGRAM 
    function in an OPTION dictionary. 
    
    INPUTS:
    option  : dictionary containing default option values
    *kwargs : variable-length keyword argument list. The keywords by 
              definition are dictionaries with keys that must correspond to 
              one of the choices given in the _default_options function.
        
    OUTPUTS:
    option : dictionary containing option values
  
    Author:
    
    Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Sep 17, 2022
    Revised on Sep 17, 2022
    '''
    
    # Check for valid keys and values in dictionary
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if optname == 'nonrmsdz':
            raise ValueError('nonrmsdz is an obsolete option. Use cmapzdata instead.')

        if not optname in option:
            raise ValueError('Unrecognized option: ' + optname)
        else:
            # Replace option value with that from arguments
            option[optname] = optvalue

            # Check values for specific options
            if optname == 'circlelinespec':
                option = _circle_color_style(option)
            elif optname == 'cmapzdata':
                if isinstance(option[optname], str):
                    raise ValueError('cmapzdata cannot be a string!')
                elif isinstance(option[optname], bool):
                    raise ValueError('cmapzdata cannot be a boolean!')
                option['cmapzdata'] = optvalue
            elif optname == 'equalaxes':
                option['equalaxes'] = check_on_off(option['equalaxes'])
            elif optname == 'markerlabel':
                if type(optvalue) is list:
                    option['markerlabel'] = optvalue
                elif type(optvalue) is dict:
                    option['markerlabel'] = optvalue
                else:
                    raise ValueError('markerlabel value is not a list or dictionary: ' +
                                     str(optvalue))
            elif optname == 'markerlegend':
                option['markerlegend'] = check_on_off(option['markerlegend'])
                
            elif optname in {'markercolors'}:
                accepted_keys = {
                    'markercolors': {'face', 'edge'},
                }
                _check_dict_with_keys(optname, option[optname],
                                      accepted_keys[optname], or_none=True)
                del accepted_keys

            elif optname == 'normalized':
                option['normalized'] = check_on_off(option['normalized'])
            elif optname == 'overlay':
                option['overlay'] = check_on_off(option['overlay'])

        del optname, optvalue   
    
    return option

def _read_options(option, **kwargs) -> dict:
    '''
    Reads the optional arguments from a CSV file. 
    
    Reads the optional arguments for target_diagram function from a 
    CSV file if a target_options_file parameter is provided that contains
    the name of a valid Comma Separated Value (CSV) file. Otherwise the
    function returns with no action taken. 
    
    INPUTS:
    option  : dictionary containing default option values

    *kwargs : variable-length keyword argument list. One of the keywords 
              must be in the list below for the function to perform any
            action.
    target_options_file : name of CSV file containing values for optional
                          arguments of the target_diagram function. If no file
                          suffix is given, a ".csv" is assumed. (Default: empty string '')
        
    OUTPUTS:
    option : dictionary containing option values
  
    Author:
    
    Peter Rochford, rochford.peter1@gmail.com

    Created on Sep 17, 2022
    Revised on Sep 17, 2022
    '''
    # Check if option filename provided
    name = ''
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if optname == 'target_options_file':
            name = optvalue 
            break 
    if not name: return option
    
    # Check if CSV file suffix
    filename, file_extension = os.path.splitext(name)
    
    if file_extension == "":
        filename = name + '.csv'
    elif name.endswith('.csv'):
        filename = name
    else:
        raise Exception("Invalid file type: " + name)
    
    # Check if file exists
    if not os.path.isfile(filename):
        raise Exception("File does not exist: " + filename)
        
    # Load object from CSV file
    objectData = pd.read_csv(filename)
    
    # Parse object for keys and values
    keys = objectData.iloc[:,0]
    values = objectData.iloc[:,1].tolist()

    # Identify keys requiring special consideration   
    listkey = ['cmapzdata', 'circles']
    tuplekey = []
    
    # Process for options read from CSV file
    for index in range(len(keys)):
        
        # Skip assignment if no value provided in CSV file
        if pd.isna(values[index]):
            continue
        
        # Convert list provided as string
        if is_list_in_string(values[index]):
            # Remove brackets
            values[index] = values[index].replace('[','').replace(']','')
         
        if keys[index] in listkey:
            if pd.isna(values[index]):
                option[keys[index]]=[]
            else:
                # Convert string to list of floats
                split_string = re.split(' |,', values[index])
                split_string = ' '.join(split_string).split()
                option[keys[index]] = [float(x) for x in split_string]
        
        elif keys[index] in tuplekey:
            try:
                option[keys[index]]=eval(values[index])
            except NameError:
                raise Exception('Invalid ' + keys[index] + ': '+ values[index])
        elif pd.isna(values[index]):
            option[keys[index]]=''
        elif is_int(values[index]):
            option[keys[index]] = int(values[index])
        elif is_float(values[index]):
            option[keys[index]] = float(values[index])
        elif values[index]=='None':
            option[keys[index]] = None
        else:
            option[keys[index]] = values[index]

    # Check values for specific options
    if option['circlelinespec']:
        option = _circle_color_style(option)

    return option

def get_target_diagram_options(**kwargs) -> dict:
    '''
    Get optional arguments for target_diagram function.
    
    Retrieves the optional arguments supplied to the TARGET_DIAGRAM 
    function as a variable-length keyword argument list (*KWARGS), and
    returns the values in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. The function will terminate
    with an error if an unrecognized optional argument is supplied.
    
    INPUTS:
    *kwargs : variable-length keyword argument list. The keywords by 
              definition are dictionaries with keys that must correspond to 
              one choices given in OUTPUTS below.
    
    OUTPUTS:
    option : dictionary containing option values. (Refer to _default_options
             and display_taylor_diagram_options functions for more information.)
  
    Authors:
    
    Peter A. Rochford
        rochford.peter1@gmail.com
    
    Created on Nov 25, 2016
    Revised on Sep 17, 2022
    '''
    from skill_metrics import check_on_off
    from matplotlib import rcParams

    nargin = len(kwargs)

    # Set default parameters for all options
    option = _default_options()

    # No options requested, so return with only defaults
    if nargin == 0: return option

    # Read the optional arguments for taylor_diagram function from a 
    # CSV file, if specified. 
    option = _read_options(option, **kwargs)

    # Check for valid keys and values in dictionary
    # Allows user to override options specified in CSV file
    option = _get_options(option, **kwargs)
    
    return option
