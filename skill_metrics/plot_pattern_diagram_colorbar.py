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
    
    The color range is controlled by option['nonRMSDz']. 
    option['colormap'] = 'on' :
        the scatter function maps the elements in Z to colors in the 
        current colormap
    option['colormap']= 'off' : the color axis is mapped to the range
        [min(Z) max(Z)]
    
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

    hp = plt.scatter(X,Y, s=markerSize, c=Z, marker = 'd')
    hp.set_facecolor(hp.get_edgecolor())
    
    # Add color bar to plot
    if option['colormap'] == 'on':
        hc = plt.colorbar(orientation='horizontal', aspect = 6,
                           fraction=0.04, pad=0.04)
        
    elif option['colormap'] == 'off':
        if len(Z) > 1:
            plt.clim(min(Z), max(Z))
            hc = plt.colorbar(orientation='horizontal', aspect = 6,
                              fraction=0.04, pad=0.04)
            hc.set_ticklabels('Min. RMSD','Max. RMSD')
    else:
        raise ValueError('Invalid option for option.colormap: ' + 
                         option['colormap']);
    
    # Set desired properties of color bar
    location = _getColorBarLocation(hc, option, xscale = 1.0,
                                   yscale = 7.5, cxscale = cxscale)
    hc.ax.set_position(location) # set new position
    hc.ax.tick_params(labelsize=fontSize) # set tick label size

    # Limit number of ticks on colar bar to 4
    hc.locator = ticker.MaxNLocator(nbins=5)
    hc.update_ticks()

    hc.ax.xaxis.set_ticks_position('top')
    hc.ax.xaxis.set_label_position('top')

    # Title the color bar
    if option['titlecolorbar']:
        hc.set_label(option['titlecolorbar'],fontsize=fontSize)
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

    # Get current position of color bar
    cp = hc.ax.get_position()

    # Calculate location
    if 'checkSTATS' in option:
        # Taylor diagram
        location = [cp.x0 + xscale*0.5*(1+math.cos(math.radians(45)))*cp.width, yscale*cp.y0,
                    cxscale*cp.width/6, cp.height]
    else:
        # target diagram
        location = [cp.x0 + xscale*0.5*(1+math.cos(math.radians(60)))*cp.width, yscale*cp.y0,
                    cxscale*cp.width/6, cxscale*cp.height]

    return location
