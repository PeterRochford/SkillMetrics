def get_single_markers(markers: dict):
#def get_single_markers(markers: dict) -> tuple[list, list, list, list, list, list]: #fails with Python 3.6
    '''
    Provides a list of markers and their properties as stored in a dictionary.
    
    Returns a list of properties for individual markers as given in the 'markers' 
    dictionary. Each marker can have its individual set of properties. 

    INPUTS:
    markers : Dictionary providing individual control of the marker
              key - text label for marker, e.g. '14197'
              key['labelColor'] - color of marker label, e.g. 'r' for red
              key['symbol'] - marker symbol, e.g. 's' for square
              key['size'] - marker size, e.g. 9
              key['faceColor'] - marker face color, e.g. 'b' for blue
              key['edgeColor'] - marker edge color, e.g. 'k' for black line
    
    OUTPUTS:
    markerlabel     : list of text labels for marker
    labelcolor      : list of color of marker label
    marker          : list of marker symbol & color
    markersize      : list of marker size
    markerfacecolor : list of marker face color
    markeredgecolor : list of marker edge color

    Authors:
    Peter A. Rochford
    rochford.peter1@gmail.com

    Created on Mar 12, 2023
    Revised on Mar 13, 2023
    '''
    if markers is None:
        raise ValueError("Empty dictionary provided for option['markers']")

    labelcolor = []
    marker = []
    markerfacecolor = []
    markeredgecolor = []
    markerlabel = []
    markersize = []
    
    # Iterate through keys in dictionary
    for key in markers:
        color = markers[key]['faceColor']
        symbol = markers[key]['symbol']
        SymbolColor = symbol + color
        marker.append(SymbolColor)
        markersize.append(markers[key]['size'])
        markerfacecolor.append(color)
        markeredgecolor.append(markers[key]['edgeColor'])
        markerlabel.append(key) # store label
        labelcolor.append(markers[key]['labelColor'])

    return markerlabel, labelcolor, marker, markersize, markerfacecolor, markeredgecolor
