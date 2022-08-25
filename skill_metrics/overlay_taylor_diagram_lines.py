from skill_metrics.get_from_dict_or_default import get_from_dict_or_default
import numpy as np
import matplotlib


def overlay_taylor_diagram_lines(ax: matplotlib.axes.Axes, axes: dict,
                                      option: dict) -> None:
    '''
    Overlay lines emanating from origin on a Taylor diagram.

    Plots lines emanating from origin to indicate correlation values (CORs) 

    It is a direct adaptation of the overlay_taylor_diagram_lines() function
    for the screnarion in which the Taylor diagram is draw in an 
    matplotlib.axes.Axes object.
 
    INPUTS:
    ax     : matplotlib.axes.Axes object in which the Taylor diagram will be plotted
    axes   : data structure containing axes information for target diagram
    cax    : handle for plot axes
    option : data structure containing option values. (Refer to 
             GET_TAYLOR_DIAGRAM_OPTIONS function for more information.)
    option['colcor']        : CORs grid and tick labels color (Default: blue)
    option['colscor']       : dictionary with two possible colors as keys ('grid',
                                'tick_labels') or None, if None then considers only the
                                value of 'colscor' (Default: None)
    option['numberpanels']  : number of panels
    option['showlabelscor'] : Show or not the CORRELATION tick labels
    option['stylecor']      : Linestyle of the CORs grid
    option['tickcor']       : CORs values to plot lines from origin
    option['widthcor']      : Line width of the CORs grid
 
    OUTPUTS:
    None.
    
    Author: Andre D. L. Zanchetta (adapting Peter A. Rochford's code)
        adlzanchetta@gmail.com

    Created on Aug 14, 2022
   '''

    # Get common information
    corr = option['tickcor'][option['numberpanels']-1]
    th  = np.arccos(corr)
    cst, snt = np.cos(th), np.sin(th)
    del th
    
    # DRAW CORRELATION LINES EMANATING FROM THE ORIGIN:
    cs = np.append(-1.0*cst, cst)
    sn = np.append(-1.0*snt, snt)
    lines_col = get_from_dict_or_default(option, 'colcor', 'colscor', 'grid')
    for i, val in enumerate(cs):
        ax.plot([0, axes['rmax']*cs[i]],
                 [0, axes['rmax']*sn[i]], 
                 linestyle = option['stylecor'],
                 color = lines_col,
                 linewidth = option['widthcor'])
        del i, val
    del lines_col, sn, cs
    
    # annotate them in correlation coefficient
    if option['showlabelscor'] == 'on':
        ticklabels_col = get_from_dict_or_default(option, 'colcor', 'colscor', 'tick_labels')
        fontSize = matplotlib.rcParams.get('font.size')
        rt = 1.05 * axes['rmax']
        for i, cc in enumerate(corr):
            if option['numberpanels'] == 2:
                x = (1.05+abs(cst[i])/30)*axes['rmax']*cst[i]
            else:
                x = rt*cst[i]
            y = rt*snt[i]
            ax.text(x, y,
                    str(round(cc, 2)),
                    horizontalalignment = 'center',
                    color = ticklabels_col,
                    fontsize = fontSize)
            del i, cc
        del fontSize, rt, ticklabels_col

    return None
