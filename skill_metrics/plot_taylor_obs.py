import matplotlib.pyplot as plt
import numpy as np

def plot_taylor_obs(ax,obsSTD, axes, option):
    '''
    Plots observation STD on Taylor diagram.
    
    Optionally plots a marker on the x-axis indicating observation STD, 
    a label for this point, and a contour circle indicating the STD 
    value.
    
    INPUTS:
    ax     : axes handle for Taylor diagram
    obsSTD : observation standard deviation
    axes   : data structure containing axes information for target diagram
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

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''
    
    if option['markerobs'] != 'none':
        plt.hold(True)

        # Display marker on x-axis indicating observed STD
        yobsSTD = 0.001*axes['rmax'] -axes['rmin']
        plt.plot(obsSTD,yobsSTD,option['markerobs'],color = option['colobs'],
                 markersize = 6, markerfacecolor = option['colobs'], 
                 markeredgecolor = option['colobs'],
                 linewidth = 1.0, clip_on=False);
    
    if option['titleobs'] != '':
        # Put label below the marker
        labelweight = 'bold'
        labelsize = ax[0].get_fontsize() - 2
        x = obsSTD; y = -0.05*axes['rmax'];
        plt.text(x,y,option['titleobs'], color = option['colobs'],
                 horizontalalignment = 'center', 
                 fontweight = labelweight, fontsize = labelsize)

    
    if option['styleobs'] != '':
        # Draw circle for observation STD
        plt.hold(True)
        theta = np.arange(0, 2*np.pi, np.pi/150)
        xunit = obsSTD*np.cos(theta)
        yunit = obsSTD*np.sin(theta)
        plt.plot(xunit,yunit,linestyle=option['styleobs'],
                 color = option['colobs'],linewidth = option['widthobs'])
