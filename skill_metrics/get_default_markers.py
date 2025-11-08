import warnings
from itertools import cycle, islice, product
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
    
    Mattia Almansi
    m.almansi@bopen.eu

    Created on Mar 12, 2023
    Revised on Nov 6, 2025
    '''

    # Define list of marker symbols and colors
    MARKERS = ["+", "o", "x", "s", "d", "^", "v", "p", "h", "*"]
    COLORS = ["r", "b", "g", "c", "m", "y", "k"]

    # Use defaults i provided
    if option['default_colors'] is not None:
        COLORS = option['default_colors']
    if option['default_markers'] is not None:
        MARKERS = option['default_markers']
        
    # Perform actions when default_colors has a value    
    # Use color list above or list supplied via option
    if len(X) <= min(len(MARKERS), len(COLORS)):
        # Fewer points than pairings of markers and colors
        if option['markercolor'] is None:
            symbols_colors = zip(MARKERS[: len(X)], COLORS[: len(X)])
            # print("1: symbols_colors = ", list(symbols_colors)) #debug
            # symbols_colors = zip(MARKERS[: len(X)], COLORS[: len(X)]) #debug
        else:
            symbols_colors = zip(MARKERS[: len(X)], [option["markercolor"]])
            # print("2: symbols_colors = ", list(symbols_colors)) #debug
            # symbols_colors = zip(MARKERS[: len(X)], [option["markercolor"]]) #debug
    else:
        # All possible pairings of markers and colors (70 pairs)
        temp = islice(cycle(product(COLORS, MARKERS)), len(X)) # (color, marker)
        symbols_colors = [item[::-1] for item in temp] # (marker, color)
        # print("3: symbols_colors = ", list(symbols_colors)) #debug
        # temp = islice(cycle(product(COLORS, MARKERS)), len(X)) # debug
        # symbols_colors = [item[::-1] for item in temp] # debug

        max_cases = len(MARKERS) * len(COLORS)
        if option["markercolor"] is None and len(X) > max_cases:
            warnings.warn(
                (
                    f"You must introduce new markers and colors to plot more than {max_cases} cases."
                    "Markers and colors are defined using global variables MARKERS and COLORS"
                ),
                UserWarning,
            )

    marker = []
    markercolor = []
    for symbol, color in symbols_colors:
        marker.append(symbol + color)
        markercolor.append(clr.to_rgba(color, option["alpha"])) # include face color transparency
    return marker, markercolor

def _disp(text):
    print(text)