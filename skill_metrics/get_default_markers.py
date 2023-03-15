import matplotlib.colors as clr

def get_default_markers(X, option: dict) -> tuple[list, list]:
    '''
    Provides a list of default markers and marker colors.
    
    Returns a list of 70 marker symbol & color combinations.

    INPUTS:
    X      : x-coordinates of markers
    option : dictionary containing option values. (Refer to 
        GET_TARGET_DIAGRAM_OPTIONS function for more information.)
    option['markercolor'] : single color to use for all markers
    option['markerlabel'] : labels for markers
    
    OUTPUTS:
    marker      : list of marker symbols
    markercolor : list of marker colors

    Authors:
    Peter A. Rochford
    rochford.peter1@gmail.com

    Created on Mar 12, 2023
    Revised on Mar 12, 2023
    '''
    # Set face color transparency
    alpha = option['alpha']

    # Define list of marker symbols and colros
    kind = ['+','o','x','s','d','^','v','p','h','*']
    colorm = ['r','b','g','c','m','y','k','gray']
    if len(X) > 80:
        _disp('You must introduce new markers to plot more than 70 cases.')
        _disp('The ''marker'' character array need to be extended inside the code.')
    
    if len(X) <= len(kind):
        # Define markers with specified color
        marker = []
        markercolor = []
        if option['markercolor'] is None:
            for i, color in enumerate(colorm):
                rgba = clr.to_rgb(color) + (alpha,)
                marker.append(kind[i] + color)
                markercolor.append(rgba)
        else:
            rgba = clr.to_rgb(option['markercolor']) + (alpha,)
            for symbol in kind:
                marker.append(symbol + option['markercolor'])
                markercolor.append(rgba)
    else:
        # Define markers and colors using predefined list
        marker = []
        markercolor = []
        for color in colorm:
            for symbol in kind:
                marker.append(symbol + color)
                rgba = clr.to_rgb(color) + (alpha,)
                markercolor.append(rgba)

    return marker, markercolor
