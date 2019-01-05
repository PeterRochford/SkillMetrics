import matplotlib.pyplot as plt
import numpy as np

def plot_taylor_obs(ax, obsSTD, axes, option):
    '''
    Plots observation STD on Taylor diagram.
    
    Optionally plots a marker on the x-axis indicating observation STD, 
    a label for this point, and a contour circle indicating the STD 
    value.
    
    INPUTS:
    ax     : axes handle for Taylor diagram
    obsSTD : observation standard deviation
    axes   : axes information of Taylor diagram
    option : data structure containing option values. (Refer to 
             GET_TAYLOR_DIAGRAM_OPTIONS function for more information.)
    option['colobs']       : color for observation labels (Default : magenta)
    option['markerobs']    : marker to use for x-axis indicating observed STD
    option['styleobs']     : line style for observation grid line
    option['titleobs']     : label for observation point label (Default: '')
    option['widthobs']     : linewidth for observation grid line (Default: .8)
 
    OUTPUTS:
    None
    
    Author: Peter A. Rochford
            Symplectic, LLC
            www.thesymplectic.com
            prochford@thesymplectic.com

    Created on Feb 19, 2017
    Revised on Jan 1, 2019

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''
    
    if option['markerobs'] != 'none':
        # Display marker on x-axis indicating observed STD
        markersize = option['markersize'] - 4
        yobsSTD = 0.001*axes['rmax'] - axes['rmin']
        plt.plot(obsSTD,yobsSTD,option['markerobs'],color = option['colobs'],
                 markersize = markersize, markerfacecolor = option['colobs'],
                 markeredgecolor = option['colobs'],
                 linewidth = 1.0, clip_on=False);
    
    if option['titleobs'] != '':
        # Put label below the marker
        labelsize = ax[0].get_fontsize() # get label size of STD axes
        plt.xlabel(option['titleobs'], color = option['colobs'],
                   fontweight = 'bold', fontsize = labelsize)
        xlabelh = plt.gca().xaxis.get_label()
        xypos = xlabelh.get_position()
        markerpos = plt.gca().transLimits.transform((obsSTD,0))
        xlabelh.set_position([markerpos[0], xypos[1]])
        xlabelh.set_horizontalalignment('center')
    
    if option['styleobs'] != '':
        # Draw circle for observation STD
        theta = np.arange(0, 2*np.pi, np.pi/150)
        xunit = obsSTD*np.cos(theta)
        yunit = obsSTD*np.sin(theta)
        plt.plot(xunit,yunit,linestyle=option['styleobs'],
                 color = option['colobs'],linewidth = option['widthobs'])
