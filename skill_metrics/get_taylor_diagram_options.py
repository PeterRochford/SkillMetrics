from skill_metrics import check_on_off
from typing import Union
import numpy as np
import os
import pandas as pd
import re

def _calc_rinc(tick : list) -> float:
    '''
    Calculate axis tick increment given list of tick values.
    
    INPUTS:
    tick: axis values at which to plot grid circles

    return: axis tick increment
    '''
    rinc  = (max(tick) - min(tick))/ len(tick)
    return rinc

def _check_dict_with_keys(variable_name: str, dict_obj: Union[dict, None],
                          accepted_keys: set, or_none: bool = False) -> None:
    '''
    Check if an argument in the form of dictionary has valid keys.
    :return: None. Raise 'ValueError' if evaluated variable is considered invalid. 
    '''
    
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

def _default_options(CORs : list) -> dict:
    '''
    Set default optional arguments for taylor_diagram function.
    
    Sets the default optional arguments for the TAYLOR_DIAGRAM 
    function in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. 
    
    INPUTS:
    CORs : values of correlations
        
    OUTPUTS:
    option : dictionary containing option values
    option['alpha']           : blending of symbol face color (0.0 
                                transparent through 1.0 opaque). (Default : 1.0)
    option['axismax']         : maximum for the radial contours
    option['checkstats']      : Check input statistics satisfy Taylor 
                                relationship (Default : 'off')
    option['cmap']            : Choice of colormap. (Default : 'jet')
    option['cmap_vmin']       : minimum range of colormap (Default : None)
    option['cmap_vmax']       : maximum range of colormap (Default : None)
    option['cmap_marker']     : maximum range of colormap (Default : None)
    option['cmapzdata']       : data values to use for color mapping of
                                markers, e.g. RMSD or BIAS. (Default empty)
                                
    option['colcor']          : color for correlation coefficient labels (Default : blue)
    option['colscor']         : dictionary with two possible colors as keys ('grid',
                                'tick_labels') or None, if None then considers only the
                                value of 'colscor' (Default: None)
    option['colframe']        : color for the y (left) and x (bottom) spines
    option['colobs']          : color for observation labels (Default : magenta)
    option['colormap']        : 'on'/'off' switch to map color shading of
                                 markers to CMapZData values ('on') or min to
                                 max range of CMapZData values ('off').
                                 (Default : 'on')
    option['colrms']          : color for RMS labels (Default : medium green)
    option['colstd']          : color for STD labels (Default : black)
    option['colsstd']         : dictionary with two possible colors keys ('ticks',
                                'tick_labels') or None, if None then considers only the
                                value of 'colstd' (Default: None)
    option['labelrms']        : RMS axis label (Default: 'RMSD')
    option['labelweight']     : weight of the x/y/angular axis labels
    option['locationcolorbar']: location for the colorbar, 'NorthOutside' or
                                 'EastOutside'

    option['markercolor']     : single color to use for all markers (Default: None)
    option['markercolors']    : dictionary with two colors as keys ('face', 'edge')
                                or None. If None or 'markerlegend' == 'on' then
                                considers only the value of 'markercolor'. (Default: None)
    option['markerdisplayed'] : markers to use for individual experiments
    option['markerlabel']     : name of the experiment to use for marker
    option['markerlabelcolor']: marker label color (Default: 'k')
    option['markerlegend']    : 'on'/'off' switch to display marker legend
                                (Default 'off')
    option['markerobs']       : marker to use for x-axis indicating observed 
                                STD. A choice of 'none' will suppress 
                                appearance of marker. (Default 'none')
    option['markers']         : Dictionary providing individual control of the marker
                               key - text label for marker, e.g. '14197'
                               key['labelColor'] - color of marker label, e.g. 'r' for red
                               key['symbol'] - marker symbol, e.g. 's' for square
                               key['size'] - marker size, e.g. 9
                               key['faceColor'] - marker face color, e.g. 'b' for blue
                               key['edgeColor'] - marker edge color, e.g. 'k' for black line
                               (Default: None)
    option['markersize']      : marker size (Default 10)
    option['markersymbol']    : marker symbol (Default '.')

    option['numberpanels']    : Number of panels to display
                                = 1 for positive correlations
                                = 2 for positive and negative correlations
                               (Default value depends on correlations (CORs))

    option['overlay']         : 'on'/'off' switch to overlay current
                                 statistics on Taylor diagram (Default 'off')
                                 Only markers will be displayed.
    option['rincrms']         : axis tick increment for RMS values
    option['rincstd']         : axis tick increment for STD values
    option['rmslabelformat']  : string format for RMS contour labels, e.g. '0:.2f'.
                                (Default '0', format as specified by str function)
 
    option['showlabelscor']   : show correlation coefficient labels 
                                (Default: 'on')
    option['showlabelsrms']   : show RMS labels (Default: 'on')
    option['showlabelsstd']   : show STD labels (Default: 'on')

    option['stylecor']        : line style for correlation coefficient grid 
                                lines (Default: dash-dot '-.')
    option['styleobs']        : line style for observation grid line. A choice of
                                empty string '' will suppress appearance of the
                                grid line (Default: '')
    option['stylerms']        : line style for RMS grid lines 
                                (Default: dash '--')
    option['stylestd']        : line style for STD grid lines 
                                (Default: dotted ':')

    option['taylor_options_file'] name of CSV file containing values for optional
                                arguments of the taylor_diagram function. If no file
                                suffix is given, a ".csv" is assumed. (Default: empty string '')

    option['tickcor'][panel]  : tick values for correlation coefficients for
                                two types of panels
    option['tickrms']         : RMS values to plot grid circles from
                                observation point 
    option['tickstd']         : STD values to plot grid circles from origin 
    option['tickrmsangle']    : tick RMS angle (Default: 135 degrees)
    option['titleColorBar']   : title for the colorbar
    option['titlecor']        : show correlation coefficient axis label 
                                (Default: 'on')
    option['titlecorshape']   : defines the shape of the label "correlation coefficient"
                                as either 'curved' or 'linear' (Default: 'curved')
    option['titleobs']        : label for observation point (Default: '')
    option['titlerms']        : show RMS axis label (Default: 'on')
    option['titlestd']        : show STD axis label (Default: 'on')
    option['titlermsdangle']  : angle at which to display the 'RMSD' label for the RMS contours
                                (Default: 160 degrees)
 
    option['widthcor']        : linewidth for correlation coefficient grid 
                                lines (Default: .8)
    option['widthobs']        : linewidth for observation grid line (Default: .8)
    option['widthrms']        : linewidth for RMS grid lines (Default: .8)
    option['widthstd']        : linewidth for STD grid lines (Default: .8)
  
    Author:
    
    Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Sep 12, 2022
    Revised on Sep 12, 2022
    '''

    from matplotlib import rcParams

    # Set default parameters for all options
    option = {}
    option['alpha'] = 1.0
    option['axismax'] = 0.0
    option['checkstats'] = 'off'
    
    option['cmap'] = 'jet'
    option['cmap_vmin'] = None
    option['cmap_vmax'] = None
    option['cmap_marker'] = 'd'    
    option['cmapzdata'] = []

    option['colcor'] = (0, 0, 1)   # blue
    option['colscor'] = None       # if None, considers 'colcor' only
    option['colobs'] = 'm'         # magenta
    option['colrms'] = (0, .6, 0)  # medium green
    option['colstd'] = (0, 0, 0)   # black
    option['colsstd'] = None       # if None, considers 'colstd' only
    option['colframe'] = '#000000' # black
    option['colormap'] = 'on'

    option['labelrms'] = 'RMSD'
    option['labelweight'] = 'bold' # weight of the x/y labels ('light', 'normal', 'bold', ...)
    option['locationcolorbar'] = 'NorthOutside'

    option['markercolor'] = None
    option['markercolors'] = None  # if None, considers 'markercolor' only
    option['markerdisplayed'] = 'marker'
    option['markerlabel'] = ''
    option['markerlabelcolor'] = 'k'
    option['markerlegend'] = 'off'
    option['markerobs'] = 'none'
    option['markers'] = None
    option['markersize'] = 10
    option['markersymbol'] = '.'

    option['titlecorshape'] = "curved"
                                
    # panels: double (2) or single (1)
    negative = CORs[np.where(CORs < 0.0)]
    option['numberpanels'] = 2 if (len(negative) > 0) else 1
    del negative

    option['overlay'] = 'off'
    option['rincrms'] = []
    option['rincstd'] = []
    option['rmslabelformat'] = '0'
 
    option['showlabelscor'] = 'on'
    option['showlabelsrms'] = 'on'
    option['showlabelsstd'] = 'on'

    option['stylecor'] = '-.'
    option['styleobs'] = ''
    option['stylerms'] = '--'
    option['stylestd'] = ':'

    option['taylor_options_file'] = ''

    # Note that "0" must be explicitly given or a scientific number is
    # stored
    tickval1 = [1, 0.99, 0.95, 0]
    middle = np.linspace(0.9, 0.1, 9)
    tickval1[3:3] = middle
    tickval2 = tickval1[:]
    values = np.linspace(-0.1,-0.9,9)
    tickval2.extend(values)
    tickval2.extend([-0.95, -0.99, -1])
    option['tickcor'] = (tickval1, tickval2) # store as tuple
    del tickval1, tickval2, middle, values

    option['tickrms'] = [] 
    option['tickstd'] = [] 
    option['tickrmsangle'] = -1
    option['titlecolorbar'] = ''
    option['titlecor'] = 'on'
    option['titleobs'] = ''
    option['titlerms'] = 'on'
    option['titlermsdangle'] = 160.0
    option['titlestd'] = 'on'
 
    lineWidth = rcParams.get('lines.linewidth')
    option['widthcor'] = lineWidth
    option['widthobs'] = lineWidth
    option['widthrms'] = lineWidth
    option['widthstd'] = lineWidth
                       
    return option

def _get_options(option : dict, **kwargs) -> dict:
    '''
    Get values for optional arguments for taylor_diagram function.
    
    Gets the default optional arguments for the TAYLOR_DIAGRAM 
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

    Created on Sep 12, 2022
    Revised on Sep 12, 2022
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
            if optname == 'tickcor':
                list1 = option['tickcor'][0]
                list2 = option['tickcor'][1]
                if option['numberpanels'] == 1:
                    list1 = optvalue
                else:
                    list2 = optvalue
                option['tickcor'] = (list1, list2)
                del list1, list2
            else:
                option[optname] = optvalue

            # Check values for specific options
            if optname == 'checkstats':
                option['checkstats'] = check_on_off(option['checkstats'])
            #what is this used for?
            elif optname == 'cmapzdata':
                if isinstance(option[optname], str):
                    raise ValueError('cmapzdata cannot be a string!')
                elif isinstance(option[optname], bool):
                    raise ValueError('cmapzdata cannot be a boolean!')
                option['cmapzdata'] = optvalue

            elif optname == 'markerlabel':
                if type(optvalue) is list:
                    option['markerlabel'] = optvalue[1:]
                elif type(optvalue) is dict:
                    option['markerlabel'] = optvalue
                else:
                    raise ValueError('markerlabel value is not a list or dictionary: ' +
                                     str(optvalue))

            elif optname == 'markerlegend':
                option['markerlegend'] = check_on_off(option['markerlegend'])

            elif optname == 'overlay':
                option['overlay'] = check_on_off(option['overlay'])

            elif optname == 'rmslabelformat':
                # Check for valid string format
                labelFormat = '{' + optvalue + '}'
                try:
                    labelFormat.format(99.0)
                except ValueError:
                    raise ValueError('Invalid string format for rmslabelformat: ' + optvalue)

            elif optname in {'showlabelscor', 'showlabelsrms', 'showlabelsstd'}:
                option[optname] = check_on_off(option[optname])

            elif optname == 'tickrms':
                option['tickrms'] = np.sort(optvalue)
                option['rincrms'] = _calc_rinc(option['tickrms'])

            elif optname == 'tickstd':
                option['tickstd'] = np.sort(optvalue)
                option['rincstd'] = _calc_rinc(option['tickstd'])

            elif optname in {'titlecor', 'titlerms', 'titlestd'}:
                option[optname] = check_on_off(option[optname])

            elif optname in {'markercolors', 'colscor', 'colsstd'}:
                accepted_keys = {
                    'markercolors': {'face', 'edge'},
                    'colscor': {'grid', 'title', 'tick_labels'},
                    'colsstd': {'grid', 'title', 'tick_labels', 'ticks'}
                }
                _check_dict_with_keys(optname, option[optname],
                                      accepted_keys[optname], or_none=True)
                del accepted_keys

        del optname, optvalue

    return option

def _read_options(option : dict, **kwargs) -> dict:
    '''
    Reads the optional arguments from a CSV file. 
    
    Reads the optional arguments for taylor_diagram function from a 
    CSV file if a taylor_options_file parameter is provided that contains
    the name of a valid Comma Separated Value (CSV) file. Otherwise the
    function returns with no action taken. 
    
    INPUTS:
    option  : dictionary containing default option values

    *kwargs : variable-length keyword argument list. One of the keywords 
              must be in the list below for the function to perform any
            action.
    taylor_options_file : name of CSV file containing values for optional
                          arguments of the taylor_diagram function. If no file
                          suffix is given, a ".csv" is assumed. (Default: empty string '')
        
    OUTPUTS:
    option : dictionary containing option values
  
    Author:
    
    Kevin Wu, kevinwu5116@gmail.com

    Created on Sep 12, 2022
    Revised on Sep 12, 2022
    '''
    # Check if option filename provided
    name = ''
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if optname == 'taylor_options_file':
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
    listkey=['cmapzdata','rincrms','rincstd','tickcor','tickrms','tickstd']
    tuplekey=['colcor','colrms','colstd']
    
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

            if keys[index] == 'tickrms':
                option['rincrms'] = _calc_rinc(option[keys[index]])
            elif keys[index] == 'tickstd':
                option['rincstd'] = _calc_rinc(option[keys[index]])

        elif keys[index] in tuplekey:
            try:
                option[keys[index]]=eval(values[index])
            except NameError:
                raise Exception('Invalid ' + keys[index] + ': '+ values[index])
        elif keys[index] == 'rmslabelformat':
            option[keys[index]]=values[index]
        elif pd.isna(values[index]):
            option[keys[index]]=''
        elif is_int(values[index]):
            option[keys[index]] = int(values[index])
        elif is_float(values[index]):
            option[keys[index]] = float(values[index])
        elif values[index]=='None':
            option[keys[index]]=None
        else:
            option[keys[index]] = values[index]
        
    return option

def get_taylor_diagram_options(*args,**kwargs) -> dict:
    '''
    Get optional arguments for taylor_diagram function.
    
    Retrieves the optional arguments supplied to the TAYLOR_DIAGRAM 
    function as a variable-length input argument list (*ARGS), and
    returns the values in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. The function will terminate
    with an error if an unrecognized optional argument is supplied.
    
    INPUTS:
    *kwargs : variable-length keyword argument list. The keywords by 
              definition are dictionaries with keys that must correspond to 
              one choices given in the _default_options function.
    
    OUTPUTS:
    option : dictionary containing option values. (Refer to _default_options
             and display_taylor_diagram_options functions for more information.)
  
    Authors:
    
    Peter A. Rochford
        rochford.peter1@gmail.com
    
    Andre D. L. Zanchetta (adapting Peter A. Rochford's code)
        adlzanchetta@gmail.com

    Created on Nov 25, 2016
    Revised on Aug 14, 2022
    '''

    CORs = args[0]
    nargin = len(kwargs)

    # Set default parameters for all options
    option = _default_options(CORs)

    # No options requested, so return with only defaults
    if nargin == 0: return option

    #Check to see if the Key for the file exist
    name = ''
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if optname == 'taylor_options_file':
            name = optvalue 
            break 
    
    if name:
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
        
        # Read the optional arguments for taylor_diagram function from a 
        # CSV file, if specified. 
        option = _read_options(option, **kwargs)

    # Check for valid keys and values in dictionary
    # Allows user to override options specified in CSV file
    option = _get_options(option, **kwargs)
                                    
    return option