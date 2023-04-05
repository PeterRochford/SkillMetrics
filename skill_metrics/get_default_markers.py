import warnings
from itertools import cycle, islice, product

import matplotlib.colors as clr

# Define list of marker symbols and colros
MARKERS = ["+", "o", "x", "s", "d", "^", "v", "p", "h", "*"]
COLORS = ["r", "b", "g", "c", "m", "y", "k"]


def get_default_markers(X, option: dict) -> tuple[list, list]:
    """
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
    """

    if len(X) <= min(len(MARKERS), len(COLORS)):
        symbols_colors = zip(MARKERS[: len(X)], COLORS[: len(X)])
    else:
        max_cases = len(MARKERS) * len(COLORS)
        symbols_colors = islice(cycle(product(MARKERS, COLORS)), len(X))
        if len(X) > max_cases:
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
        rgba = clr.to_rgb(color) + (option["alpha"],)
        markercolor.append(rgba)
    return marker, markercolor
