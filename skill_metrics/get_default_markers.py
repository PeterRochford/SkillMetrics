import warnings
from itertools import cycle, islice, product

import matplotlib.colors as clr
from matplotlib.lines import Line2D


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
    # Define list of marker symbols and colros
    kind = []
    for marker in Line2D.filled_markers:
        if marker == ".":
            # Too similar to "o"
            continue
        if marker.islower() and marker.upper() in Line2D.filled_markers:
            # E.g., h and H are too similar
            continue
        kind.append(marker)

    if option["markercolor"] is None:
        colorm = [color for color in clr.BASE_COLORS if color != "w"]
    else:
        colorm = [option["markercolor"]]

    max_cases = len(kind) * len(colorm)
    if len(X) > max_cases:
        warnings.warn(
            (
                f"You must introduce new markers to plot more than {max_cases} cases."
                "The marker character array need to be extended inside the code."
            ),
            UserWarning,
        )

    marker = []
    markercolor = []
    for symbol, color in islice(cycle(product(kind, colorm)), len(X)):
        marker.append(symbol + color)
        rgba = clr.to_rgb(color) + (option["alpha"],)
        markercolor.append(rgba)
    return marker, markercolor
