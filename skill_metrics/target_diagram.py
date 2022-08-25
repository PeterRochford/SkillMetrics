from array import array
import matplotlib.pyplot as plt
import numbers
import numpy as np

from skill_metrics import get_target_diagram_axes
from skill_metrics import get_target_diagram_options
from skill_metrics import overlay_target_diagram_circles
from skill_metrics import plot_pattern_diagram_colorbar
from skill_metrics import plot_pattern_diagram_markers
from skill_metrics import plot_target_axes

def _display_target_diagram_options():
    '''
    Displays available options for TARGET_DIAGRAM function.
    '''

    _disp('General options:')
    _dispopt("'colormap'","'on'/ 'off' (default): "  + 
        "Switch to map color shading of markers to colormap ('on')\n\t\t"  +
        "or min to max range of RMSDz values ('off').")
    _dispopt("'overlay'","'on' / 'off' (default): " + 
            'Switch to overlay current statistics on target diagram. ' +
            '\n\t\tOnly markers will be displayed.')
    _disp("OPTIONS when 'colormap' == 'on'")
    _dispopt("'cmap'","Choice of colormap. (Default: 'jet')")
    _dispopt("'cmap_marker'","Marker to use with colormap (Default: 'd')")
    _dispopt("'cmap_vmax'","Maximum range of colormap (Default: None)")
    _dispopt("'cmap_vmax'","Minimum range of colormap (Default: None)")
    _disp('')
    
    _disp('Marker options:')
    _dispopt("'MarkerDisplayed'", 
        "'marker' (default): Experiments are represented by individual symbols\n\t\t" +
        "'colorBar': Experiments are represented by a color described " + 
        'in a colorbar')
    _disp("OPTIONS when 'MarkerDisplayed' == 'marker'")
    _dispopt("'markerColor'",'Marker color')
    _dispopt("'markerColors'","Dictionary with two colors as keys ('face', 'edge')" +
             "or None." + "\n\t\t" + 
             "If None or 'markerlegend' == 'on' then considers only the value of " + 
             "'markerColor'. (Default: None)")
    _dispopt("'markerLabel'",'Labels for markers')
    _dispopt("'markerLabelColor'",'Marker label color (Default: black)')
    _dispopt("'markerLegend'","'on' / 'off' (default): Use legend for markers'")
    _dispopt("'markerSize'",'Marker size (Default: 10)')
    _dispopt("'markerSymbol'","Marker symbol (Default: '.')")
    
    _disp("OPTIONS when 'MarkerDisplayed' == 'colorbar'")
    _dispopt("'cmapZData'","Data values to use for " +
            'color mapping of markers, e.g. RMSD or BIAS.\n\t\t' +
            '(Used to make range of RMSDs values appear above color bar.)')
    _dispopt("'locationColorBar'","Location for the colorbar, 'NorthOutside' " +
             "or 'EastOutside'")
    _dispopt("'titleColorBar'",'Title of the colorbar.')
    _disp('')
     
    _disp('Axes options:')
    _dispopt("'axismax'",'Maximum for the Bias & uRMSD axis')
    _dispopt("'colFrame'",'Color for the y and x spines')
    _dispopt("'equalAxes'","'on' (default) / 'off': Set axes to be equal")
    _dispopt("'labelWeight'","Weight of the x & y axis labels")
    _dispopt("'ticks'",'Define tick positions ' +
            '(default is that used by axis function)')
    _dispopt("'xtickLabelPos'",'position of the tick labels ' +
            'along the x-axis (empty by default)')
    _dispopt("'ytickLabelPos'",'position of the tick labels ' +
            'along the y-axis (empty by default)')
    _disp('')
     
    _disp('Diagram options:')
    _dispopt("'alpha'","Blending of symbol face color (0.0 transparent through 1.0 opaque)" +
             "\n\t\t" + "(Default: 1.0)")
    _dispopt("'circles'",'Define the radii of circles to draw ' +
            '(default of (maximum RMSDs)*[.7 1], [.7 1] when normalized diagram)')
    _dispopt("'circleColor'",'Circle line color specification (default None)')
    _dispopt("'circleCols'","Dictionary with two possible colors keys ('ticks'," +
             "'tick_labels')" +
             "\n\t\t or None, if None then considers only the value of 'circlecolor'" +
             "(Default: None)")
    _dispopt("'circleLineSpec'",'Circle line specification (default ' +
            "dashed black, '--k')")
    _dispopt("'circleLineWidth'",'Circle line width')
    _dispopt("'circleStyle'",'Line style for circles, e.g. "--" (Default: None)')
    _dispopt("'normalized'","'on' / 'off' (default): normalized target diagram")
    _dispopt("'obsUncertainty'",'Observational Uncertainty (default of 0)')

def _disp(text):
    print(text)

def _dispopt(optname,optval):
    '''
    Displays option name and values

    This is a support function for the DISPLAY_TARGET_DIAGRAM_OPTIONS function.
    It displays the option name OPTNAME on a line by itself followed by its 
    value OPTVAL on the following line.
    '''

    _disp('\t%s' % optname)
    _disp('\t\t%s' % optval)

def _ensure_np_array_or_die(v, label: str) -> np.ndarray:
     '''
     Check variable has is correct data type.
     
     v: Value to be ensured
     label: Python data type
     '''

     ret_v = v
     if isinstance(ret_v, array):
         ret_v = np.array(v)
     if isinstance(ret_v, numbers.Number):
         ret_v = np.array(v, ndmin=1)
     if not isinstance(ret_v, np.ndarray):
         raise ValueError('Argument {0} is not a numeric array: {1}'.format(label, v))
     return ret_v

def _get_target_diagram_arguments(*args):
    '''
    Get arguments for target_diagram function.
    
    Retrieves the arguments supplied to the TARGET_DIAGRAM function as
    arguments and displays the optional arguments if none are supplied.
    Otherwise, tests the first 3 arguments are numeric quantities and 
    returns their values.
    
    INPUTS:
    args : variable-length input argument list
    
    OUTPUTS:
    Bs    : Bias (B) or Normalized Bias (B*). Plotted along y-axis
            as "Bias".
    RMSDs : unbiased Root-Mean-Square Difference (RMSD') or normalized
            unbiased Root-Mean-Square Difference (RMSD*'). Plotted along 
            x-axis as "uRMSD".
    RMSDz : total Root-Mean-Square Difference (RMSD). Labeled on plot as "RMSD".
    '''

     # Check amount of values provided and display options list if needed
    import numbers
        
    nargin = len(args)
    if nargin == 0:
        # Display options list
        _display_target_diagram_options()
        return [], [], [], []
    elif nargin == 3:
        bs, rmsds, rmsdz = args
        CAX = plt.gca()
    elif nargin == 4:
        CAX, bs, rmsds, rmsdz = args
        if not hasattr(CAX, 'axes'):
            raise ValueError('First argument must be a matplotlib axes.')
    else:
        raise ValueError('Must supply 3 or 4 arguments.')
    del nargin
        
    # Check data validity
    Bs = _ensure_np_array_or_die(bs, "Bs")
    RMSDs = _ensure_np_array_or_die(rmsds, "RMSDs")
    RMSDz = _ensure_np_array_or_die(rmsdz, "RMSDz")

    return CAX, Bs, RMSDs, RMSDz

def target_diagram(*args, **kwargs):
    '''
    Plot a target diagram from statistics of different series.
    
    target_diagram(Bs,RMSDs,RMSDz,keyword=value)
    
    The first 3 arguments must be the inputs as described below followed by
    keywords in the format OPTION = value. An example call to the function 
    would be:
    
    target_diagram(Bs,RMSDs,RMSDz,markerdisplayed='marker')
    
    INPUTS:
    Bs    : Bias (B) or Normalized Bias (B*). Plotted along y-axis
            as "Bias".
    RMSDs : unbiased Root-Mean-Square Difference (RMSD') or normalized
            unbiased Root-Mean-Square Difference (RMSD*'). Plotted along 
            x-axis as "uRMSD".
    RMSDz : total Root-Mean-Square Difference (RMSD). Labeled on plot as "RMSD".
    
    OUTPUTS:
    None.
    
    LIST OF OPTIONS:
    For an exhaustive list of options to customize your diagram, call the 
    function without arguments at a Python command line:
    % python
    >>> import skill_metrics as sm
    >>> sm.target_diagram()
    
    Reference:
 
    Jolliff, J. K., J. C. Kindle, I. Shulman, B. Penta, M. Friedrichs, 
      R. Helber, and R. Arnone (2009), Skill assessment for coupled 
      biological/physical models of marine systems, J. Mar. Sys., 76(1-2),
      64-82, doi:10.1016/j.jmarsys.2008.05.014

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Nov 25, 2016
    '''

     # Check for no arguments
    if len(args) == 0: return
        
    # Process arguments (if given)
    ax, Bs, RMSDs, RMSDz = _get_target_diagram_arguments(*args)

    # Get options
    option = get_target_diagram_options(**kwargs)

    #  Get axis values for plot
    axes = get_target_diagram_axes(RMSDs,Bs,option)

    # Overlay circles
    overlay_target_diagram_circles(ax, option)

    # Modify axes for target diagram (no overlay)
    if option['overlay'] == 'off':
        axes_handles = plot_target_axes(ax, axes)

    # Plot data points
    lowcase = option['markerdisplayed'].lower()
    if lowcase == 'marker':
        plot_pattern_diagram_markers(ax,RMSDs,Bs,option)
    elif lowcase == 'colorbar':
        plot_pattern_diagram_colorbar(ax,RMSDs,Bs,RMSDz,option)
    else:
        raise ValueError('Unrecognized option: ' + 
                         option['markerdisplayed'])
