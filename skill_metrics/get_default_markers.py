import warnings
from itertools import cycle, islice, product

import matplotlib.colors as clr

# Define list of marker symbols and colors
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
    colors = COLORS if option["markercolor"] is None else [option["markercolor"]]

    if len(X) <= min(len(MARKERS), len(colors)):
        symbols_colors = zip(MARKERS[: len(X)], colors[: len(X)])
    else:
        symbols_colors = islice(cycle(product(MARKERS, colors)), len(X))
        max_cases = len(MARKERS) * len(colors)
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
        markercolor.append(clr.to_rgba(color, option["alpha"]))
    return marker, markercolor
