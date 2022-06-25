import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import ticker
import math

def plot_pattern_diagram_colorbar(X,Y,Z,option):
    '''
    Plots color markers on a pattern diagram shaded according to a 
    supplied value.
    
    Values are indicated via a color bar on the plot.
    
    Plots color markers on a target diagram according their (X,Y) locations.
    The color shading is accomplished by plotting the markers as a scatter 
    plot in (X,Y) with the colors of each point specified using Z as a 
    vector.
    
    The color range is controlled by option['cmapzdata'].
    option['colormap'] = 'on' :
        the scatter function maps the elements in Z to colors in the 
        current colormap
    option['colormap']= 'off' : the color axis is mapped to the range
        [min(Z) max(Z)]       
    option.locationColorBar   : location for the colorbar, 'NorthOutside'
                                or 'eastoutside'
    
    The color bar is titled using the content of option['titleColorBar'] 
    (if non-empty string).
    
    INPUTS:
    x : x-coordinates of markers
    y : y-coordinates of markers
    z : z-coordinates of markers (used for color shading)
    option : dictionary containing option values.
    option['colormap'] : 'on'/'off' switch to map color shading of markers 
        to colormap ('on') or min to max range of Z values ('off').
    option['titleColorBar'] : title for the color bar
    
    OUTPUTS:
    None.
    
    Created on Nov 30, 2016
    Revised on Jan 1, 2019
    
    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''

    '''
    Plot color shaded data points using scatter plot
    Keyword s defines marker size in points^2
            c defines the sequence of numbers to be mapped to colors 
              using the cmap and norm
    '''
    fontSize = rcParams.get('font.size')
    cxscale = fontSize/10 # scale color bar by font size
    markerSize = option['markersize']**2

    hp = plt.scatter(X,Y, s=markerSize, c=Z, marker=option['cmap_marker'],
                      cmap=option['cmap'], vmin=option['cmap_vmin'],
                      vmax=option['cmap_vmax'])
    
    hp.set_facecolor(hp.get_edgecolor())
    
    # Set parameters for color bar location
    location = option['locationcolorbar'].lower()
    xscale= 1.0
    labelpad = -25
    if location == 'northoutside':
        orientation = 'horizontal'
        aspect = 6
        fraction = 0.04
    elif location == 'eastoutside':
        orientation = 'vertical'
        aspect = 25
        fraction = 0.15
        if 'checkstats' in option:
            # Taylor diagram
            xscale = 0.5
            cxscale = 6*fontSize/10
            labelpad = -30
    else:
        raise ValueError('Invalid color bar location: ' + option['locationcolorbar']);
    
    # Add color bar to plot
    if option['colormap'] == 'on':
        # map color shading of markers to colormap 
        hc = plt.colorbar(orientation = orientation, aspect = aspect,
                          fraction = fraction, pad=0.06)

        # Limit number of ticks on color bar to reasonable number
        if orientation == 'horizontal':
            _setColorBarTicks(hc,5,20)
        
    elif option['colormap'] == 'off':
        # map color shading of markers to min to max range of Z values
        if len(Z) > 1:
            plt.clim(min(Z), max(Z))
            hc = plt.colorbar(orientation = orientation, aspect = aspect,
                            fraction = fraction, pad=0.06, ticks=[min(Z), max(Z)])
            
            # Label just min/max range
            hc.set_ticklabels(['Min.', 'Max.'])
    else:
        raise ValueError('Invalid option for option.colormap: ' + 
                         option['colormap']);
    
    if orientation == 'horizontal':
        location = _getColorBarLocation(hc, option, xscale = xscale,
                                       yscale = 7.5, cxscale = cxscale)
    else:
        location = _getColorBarLocation(hc, option, xscale = xscale,
                                       yscale = 1.0, cxscale = cxscale)

    hc.ax.set_position(location) # set new position
    hc.ax.tick_params(labelsize=fontSize) # set tick label size

    hc.ax.xaxis.set_ticks_position('top')
    hc.ax.xaxis.set_label_position('top')

    # Title the color bar
    if option['titlecolorbar']:
        if orientation == 'horizontal':
            hc.set_label(option['titlecolorbar'],fontsize=fontSize)
        else:
            hc.set_label(option['titlecolorbar'],fontsize=fontSize, 
                         labelpad=labelpad, y=1.05, rotation=0)
    else:
        hc.set_label(hc,'Color Scale',fontsize=fontSize)

def _getColorBarLocation(hc,option,**kwargs):
    '''
    Determine location for color bar.
    
    Determines location to place color bar for type of plot:
    target diagram and Taylor diagram. Optional scale arguments
    (xscale,yscale,cxscale) can be supplied to adjust the placement of
    the colorbar to accommodate different situations.

    INPUTS:
    hc     : handle returned by colorbar function
    option : dictionary containing option values. (Refer to 
             display_target_diagram_options function for more 
             information.)
    
    OUTPUTS:
    location : x, y, width, height for color bar
    
    KEYWORDS:
    xscale  : scale factor to adjust x-position of color bar
    yscale  : scale factor to adjust y-position of color bar
    cxscale : scale factor to adjust thickness of color bar
    '''

    # Check for optional arguments and set defaults if required
    if 'xscale' in kwargs:
        xscale = kwargs['xscale']
    else:
        xscale = 1.0
    if 'yscale' in kwargs:
        yscale = kwargs['yscale']
    else:
        yscale = 1.0
    if 'cxscale' in kwargs:
        cxscale = kwargs['cxscale']
    else:
        cxscale = 1.0

    # Get original position of color bar and not modified position
    # because of Axes.apply_aspect being called.
    cp = hc.ax.get_position(original=True)

    # Calculate location : [left, bottom, width, height]
    if 'checkstats' in option:
        # Taylor diagram
        location = [cp.x0 + xscale*0.5*(1+math.cos(math.radians(45)))*cp.width, yscale*cp.y0,
                    cxscale*cp.width/6, cp.height]
    else:
        # target diagram
        location = [cp.x0 + xscale*0.5*(1+math.cos(math.radians(60)))*cp.width, yscale*cp.y0,
                    cxscale*cp.width/6, cxscale*cp.height]

    return location

def _setColorBarTicks(hc,numBins,lenTick):
    '''
    Determine number of ticks for color bar.
    
    Determines number of ticks for colorbar so tick labels do not
    overlap.

    INPUTS:
    hc      : handle of colorbar
    numBins : number of bins to use for determining number of 
              tick values using ticker.MaxNLocator
    lenTick : maximum number of characters for all the tick labels
    
    OUTPUTS:
    None

    '''

    maxChar = 10
    lengthTick = lenTick
    while lengthTick > maxChar:
        # Limit number of ticks on color bar to numBins-1
        hc.locator = ticker.MaxNLocator(nbins=numBins, prune = 'both')
        hc.update_ticks()
        
        # Check number of characters in tick labels is 
        # acceptable, otherwise reduce number of bins
        locs = str(hc.get_ticks())
        locs = locs[1:-1].split()
        lengthTick = 0
        for tick in locs:
            tickStr = str(tick).rstrip('.')
            lengthTick += len(tickStr)
        if lengthTick > maxChar: numBins -=1
