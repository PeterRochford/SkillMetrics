from typing import Union

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

def get_target_diagram_options(**kwargs):
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
    option['markerlegend']    : 'on'/'off' switch to display marker legend
                                (Default 'off')
    option['markersize']      : marker size (Default 10)
    option['markersymbol']    : marker symbol (Default 'o')

    option['normalized']      : statistics supplied are normalized with 
                                respect to the standard deviation of reference
                                values (Default 'off')
    option['obsUncertainty']  : Observational Uncertainty (default of 0)
    option['overlay']         : 'on'/'off' switch to overlay current
                                statistics on Taylor diagram (Default 'off')
                                Only markers will be displayed.

    option['ticks']           : define tick positions (default is that used 
                                by the axis function)
    option['titlecolorbar']   : title for the colorbar
    option['xticklabelpos']   : position of the tick labels along the x-axis 
                                (empty by default)
    option['yticklabelpos']   : position of the tick labels along the y-axis 
                                (empty by default)
  
    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Nov 25, 2016
    '''
    from skill_metrics import check_on_off
    from matplotlib import rcParams

    nargin = len(kwargs)

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
    option['equalaxes'] = 'on'
    
    option['labelweight'] = 'bold' # weight of the x/y labels ('light', 'normal', 'bold', ...)
    option['locationcolorbar'] = 'NorthOutside'

    option['markercolor'] = None
    option['markercolors'] = None  # if None, considers 'markercolor' only
    option['markerdisplayed'] = 'marker'
    option['markerlabel'] = ''
    option['markerlabelcolor'] = 'k'
    option['markerlegend'] = 'off'
    option['markerobs'] = 'none'
    option['markersize'] = 10
    option['markersymbol'] = 'o'

    option['normalized'] = 'off'
    option['obsuncertainty'] = 0.0
    option['overlay'] = 'off'
    
    option['stylebias'] = '-.'
    
    option['ticks'] = []
    option['titlecolorbar'] = ''
    option['xticklabelpos'] = []
    option['yticklabelpos'] = []
    if nargin == 0:
        # No options requested, so return with only defaults
        return option
    
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
                # decipher into color and style components
                if optvalue[-1].isalpha():
                    option['circlecolor'] = optvalue[-1]
                    option['circlestyle'] =  optvalue[0:-1]
                else:
                    option['circlecolor'] = optvalue[0]
                    option['circlestyle'] =  optvalue[1:]
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
