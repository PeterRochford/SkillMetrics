import numpy as np
import matplotlib

def plot_taylor_obs(ax: matplotlib.axes.Axes, axes_handle: list, obsSTD,
                       axes_info: dict, option: dict) -> None:
    '''
    Plots observation STD on Taylor diagram.
    
    Optionally plots a marker on the x-axis indicating observation STD, 
    a label for this point, and a contour circle indicating the STD 
    value.
    
    INPUTS:
    ax     : the matplotlib.axes.Axes in which the Taylor diagram will be plotted
    obsSTD : observation standard deviation
    axes   : axes information of Taylor diagram
    option : data structure containing option values. (Refer to 
             get_taylor_diagram_subplot_options() function for more information.)
    option['colobs']       : color for observation labels (Default : magenta)
    option['markerobs']    : marker to use for x-axis indicating observed STD
    option['styleobs']     : line style for observation grid line
    option['titleobs']     : label for observation point label (Default: '')
    option['widthobs']     : linewidth for observation grid line (Default: .8)
 
    OUTPUTS:
    None
    
    Authors:
    Peter A. Rochford
    rochford.peter1@gmail.com

    Andre D. L. Zanchetta (adapting Peter A. Rochford's code)
        adlzanchetta@gmail.com

    Created on Feb 19, 2017
    Revised on Aug 14, 2022
    '''
    
    if option['markerobs'] != 'none':
        # Display marker on x-axis indicating observed STD
        markersize = option['markersize'] - 4
        yobsSTD = 0.001*axes_info['rmax'] - axes_info['rmin']
        ax.plot(obsSTD,yobsSTD,option['markerobs'],color = option['colobs'],
                 markersize = markersize, markerfacecolor = option['colobs'],
                 markeredgecolor = option['colobs'],
                 linewidth = 1.0, clip_on=False);
    
    if option['titleobs'] != '':
        # Put label below the marker
        labelsize = axes_handle[0].get_fontsize() # get label size of STD axes
        ax.set_xlabel(option['titleobs'], color = option['colobs'],
                   fontweight = 'bold', fontsize = labelsize)
        xlabelh = ax.xaxis.get_label()
        xypos = xlabelh.get_position()
        markerpos = ax.transLimits.transform((obsSTD,0))
        xlabelh.set_position([markerpos[0], xypos[1]])
        xlabelh.set_horizontalalignment('center')
    
    if option['styleobs'] != '':
        # Draw circle for observation STD
        theta = np.arange(0, 2*np.pi, np.pi/150)
        xunit = obsSTD*np.cos(theta)
        yunit = obsSTD*np.sin(theta)
        ax.plot(xunit,yunit,linestyle=option['styleobs'],
                 color = option['colobs'],linewidth = option['widthobs'])
