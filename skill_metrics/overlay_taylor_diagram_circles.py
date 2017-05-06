import matplotlib.pyplot as plt
import numpy as np
from numpy import where
from math import atan2

def overlay_taylor_diagram_circles(axes,cax,option):
    '''
    Overlays circle contours on a Taylor diagram.
    
    Plots circle contours on a Taylor diagram to indicate root mean square 
    (RMS) and standard deviation values.
    
    INPUTS:
    axes   : data structure containing axes information for Taylor diagram
    cax    : handle for plot axes
    option : data structure containing option values. (See 
             GET_TAYLOR_DIAGRAM_OPTIONS for more information.)
    option['colrms']       : RMS grid and tick labels color (Default: green)
    option['rincrms']      : Increment spacing for RMS grid
    option['stylerms']     : Linestyle of the RMS grid
    option['tickrms']      : RMS values to plot gridding circles from 
                             observation point
    option['tickRMSangle'] : Angle for RMS tick labels with the observation 
                             point (Default: 135 deg.)
    option['wi%    dthrms']     : Line width of the RMS grid
 
    option['colstd']       : STD grid and tick labels color (Default: black)
    option['rincstd']      : Increment spacing for STD grid
    option['stylestd']     : Linestyle of the STD grid
    option['tickstd']      : STD values to plot gridding circles from origin
    option['tickstdangle'] : Angle for STD tick labels with the observation 
                             point (Default: .8)
    option['widthstd']     : Line width of the STD grid
 
    OUTPUTS:
    None.
 
    See also GET_TAYLOR_DIAGRAM_OPTIONS

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''

    th = np.arange(0, 2*np.pi, np.pi/150)
    xunit = np.cos(th)
    yunit = np.sin(th)

    # now really force points on x/y axes to lie on them exactly
    inds = range(0,len(th),(len(th)-1) // 4)
    xunit[inds[1:3:2]] = np.zeros(2)
    yunit[inds[0:4:2]] = np.zeros(3)
    
    # DRAW RMS CIRCLES:
    # ANGLE OF THE TICK LABELS
    if option['tickrmsangle'] > 0:
        tickRMSAngle = option['tickrmsangle']
    else:
        phi = np.arctan2(option['tickstd'][-1],axes['dx'])
        tickRMSAngle = 180 - np.rad2deg(phi)
    
    c82 = np.cos(tickRMSAngle*np.pi/180)
    s82 = np.sin(tickRMSAngle*np.pi/180)
    radius = np.sqrt(axes['dx']**2+axes['rmax']**2 - 
                     2*axes['dx']*axes['rmax']*xunit)

    # Define label format
    labelFormat = '{' + option['rmslabelformat'] + '}'
    
    for iradius in option['tickrms']:
        phi = th[np.where(radius >= iradius)]
        phi = phi[0]
        ig = np.where(iradius*np.cos(th)+axes['dx'] <= 
                      axes['rmax']*np.cos(phi))
        hhh = plt.plot(xunit[ig]*iradius+axes['dx'],yunit[ig]*iradius, 
                       linestyle = option['stylerms'],color = option['colrms'], 
                       linewidth = option['widthrms'])
        if option['showlabelsrms'] == 'on':
            xtextpos = (iradius+option['rincrms']/20)*c82 + axes['dx']
            ytextpos = (iradius+option['rincrms']/20)*s82
            plt.text(xtextpos,ytextpos, '  ' + labelFormat.format(iradius), 
                     verticalalignment = 'baseline', 
                     color = option['colrms'], rotation = tickRMSAngle - 90)
    
    # DRAW STD CIRCLES:
    # draw radial circles
    for i in option['tickstd']:
        hhh = plt.plot(xunit*i,yunit*i,linestyle = option['stylestd'],
                   color = option['colstd'], linewidth = option['widthstd'])
        if option['showlabelsstd'] == 'on':
            if option['numberpanels'] == 2:
                if len(where(option['tickstd']==0)) == 0:
                    plt.text(0,-axes['rinc']/20,'0', verticalalignment = 'top',
                         horizontalalignment = 'center', color = option['colstd'])
                plt.text(i,-axes['rinc']/20,str(i), verticalalignment = 'top',
                     horizontalalignment = 'center', color = option['colstd'])
                plt.text(-i,-axes['rinc']/20,str(i), verticalalignment = 'top',
                     horizontalalignment = 'center', color = option['colstd'])
            else:
                if len(where(option['tickstd']==0)) == 0:
                    plt.text(-axes['rinc']/20,axes['rinc']/20,'0', 
                        verticalalignment = 'center', 
                        horizontalalignment = 'right',
                        color = option['colstd'])
                plt.text(-axes['rinc']/20,i, str(i), 
                        verticalalignment = 'center',
                        horizontalalignment = 'right',
                        color = option['colstd'])

    hhh[0].set_linestyle('-') # Make outermost STD circle solid
    
    # Draw circle for outer boundary
    i = option['axismax']
    hhh = plt.plot(xunit*i,yunit*i,linestyle = option['stylestd'],
               color = option['colstd'], linewidth = option['widthstd'])
