import matplotlib.pyplot as plt
import matplotlib
import numpy as np

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
    option['widthrms']     : Line width of the RMS grid
 
    option['colstd']       : STD grid and tick labels color (Default: black)
    option['rincstd']      : Increment spacing for STD grid
    option['stylestd']     : Linestyle of the STD grid
    option['tickstd']      : STD values to plot gridding circles from origin
    option['tickstdangle'] : Angle for STD tick labels with the observation 
                             point (Default: .8)
    option['widthstd']     : Line width of the STD grid
 
    OUTPUTS:
    None
 
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
    xunit[inds[1:5:2]] = np.zeros(2)
    yunit[inds[0:6:2]] = np.zeros(3)
    
    # DRAW RMS CIRCLES:
    # ANGLE OF THE TICK LABELS
    if option['tickrmsangle'] > 0:
        tickRMSAngle = option['tickrmsangle']
    else:
        phi = np.arctan2(option['tickstd'][-1],axes['dx'])
        tickRMSAngle = 180 - np.rad2deg(phi)
    
    cst = np.cos(tickRMSAngle*np.pi/180)
    snt = np.sin(tickRMSAngle*np.pi/180)
    radius = np.sqrt(axes['dx']**2+axes['rmax']**2 - 
                     2*axes['dx']*axes['rmax']*xunit)

    # Define label format
    labelFormat = '{' + option['rmslabelformat'] + '}'
    fontSize = matplotlib.rcParams.get('font.size') + 2
    
    for iradius in option['tickrms']:
        phi = th[np.where(radius >= iradius)]
        if len(phi) != 0:
            phi = phi[0]
            ig = np.where(iradius*np.cos(th)+axes['dx'] <=
                          axes['rmax']*np.cos(phi))
            hhh = plt.plot(xunit[ig]*iradius+axes['dx'],yunit[ig]*iradius,
                           linestyle = option['stylerms'],color = option['colrms'],
                           linewidth = option['widthrms'])
            if option['showlabelsrms'] == 'on':
                rt = (iradius+option['rincrms']/20)
                if option['tickrmsangle'] > 90:
                    xtextpos = (rt + abs(cst)*axes['rinc']/5)*cst + axes['dx']
                    ytextpos = (rt + abs(cst)*axes['rinc']/5)*snt
                else:
                    xtextpos = rt*cst + axes['dx']
                    ytextpos = rt*snt
                plt.text(xtextpos,ytextpos, '  ' + labelFormat.format(iradius),
                         horizontalalignment = 'center', verticalalignment = 'baseline',
                         color = option['colrms'], rotation = tickRMSAngle - 90,
                         fontsize = fontSize)
    
    # DRAW STD CIRCLES:
    # draw radial circles
    for i in option['tickstd']:
        hhh = plt.plot(xunit*i,yunit*i,linestyle = option['stylestd'],
                   color = option['colstd'], linewidth = option['widthstd'])

    # Set tick values for axes
    tickValues = []
    if option['showlabelsstd'] == 'on':
        if option['numberpanels'] == 2:
            tickValues = -option['tickstd'] + option['tickstd']
            tickValues.sort()
        else:
            tickValues = option['tickstd']

    plt.xticks(tickValues)

    hhh[0].set_linestyle('-') # Make outermost STD circle solid
    
    # Draw circle for outer boundary
    i = option['axismax']
    hhh = plt.plot(xunit*i,yunit*i,linestyle = option['stylestd'],
               color = option['colstd'], linewidth = option['widthstd'])
