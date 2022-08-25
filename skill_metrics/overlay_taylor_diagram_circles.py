from skill_metrics import get_from_dict_or_default
import numpy as np
import matplotlib

def overlay_taylor_diagram_circles(ax: matplotlib.axes.Axes, axes: dict,
                                        option: dict) -> None:
    '''
    Overlays circle contours on a Taylor diagram.
    
    Plots circle contours on a Taylor diagram to indicate root mean square 
    (RMS) and standard deviation values.
    
    INPUTS:
    ax     : matplotlib.axes.Axes object in which the Taylor diagram will be
             plotted
    axes   : data structure containing axes information for Taylor diagram
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
    option['colsstd']      : dictionary with two possible colors keys ('ticks',
                                'tick_labels') or None, if None then considers only the
                                value of 'colsstd' (Default: None)
    option['rincstd']      : Increment spacing for STD grid
    option['stylestd']     : Linestyle of the STD grid
    option['tickstd']      : STD values to plot gridding circles from origin
    option['tickstdangle'] : Angle for STD tick labels with the observation 
                             point (Default: .8)
    option['widthstd']     : Line width of the STD grid
 
    OUTPUTS:
    None
 
    See also GET_TAYLOR_DIAGRAM_OPTIONS

    Author: Andre D. L. Zanchetta (adapting Peter A. Rochford's code)
        adlzanchetta@gmail.com
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
            hhh = ax.plot(xunit[ig]*iradius+axes['dx'],yunit[ig]*iradius,
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

                ax.text(xtextpos, ytextpos, labelFormat.format(iradius),
                        horizontalalignment = 'center', verticalalignment = 'center',
                        color = option['colrms'], rotation = tickRMSAngle - 90,
                        fontsize = fontSize)
    
    # DRAW STD CIRCLES:
    # draw radial circles
    grid_color = get_from_dict_or_default(option, 'colstd', 'colsstd', 'grid')
    for i in option['tickstd']:
        hhh = ax.plot(xunit*i, yunit*i,
                      linestyle=option['stylestd'],
                      color=grid_color,
                      linewidth=option['widthstd'])
        del i

    # Set tick values for axes
    tickValues = []
    if option['showlabelsstd'] == 'on':
        if option['numberpanels'] == 2:
            tickValues = -option['tickstd'] + option['tickstd']
            tickValues.sort()
        else:
            tickValues = option['tickstd']

    ax.set_xticks(tickValues)

    hhh[0].set_linestyle('-') # Make outermost STD circle solid
    
    # Draw circle for outer boundary
    i = option['axismax']
    hhh = ax.plot(xunit*i, yunit*i, 
                  linestyle = option['stylestd'],
                  color = grid_color,
                  linewidth = option['widthstd'])

    return None