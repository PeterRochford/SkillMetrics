from array import array
import matplotlib.pyplot as plt
import numbers
import numpy as np

from skill_metrics import check_taylor_stats
from skill_metrics import get_taylor_diagram_axes
from skill_metrics import get_taylor_diagram_options
from skill_metrics import overlay_taylor_diagram_circles
from skill_metrics import overlay_taylor_diagram_lines
from skill_metrics import plot_pattern_diagram_colorbar
from skill_metrics import plot_pattern_diagram_markers
from skill_metrics import plot_taylor_axes
from skill_metrics import plot_taylor_obs

def _display_taylor_diagram_options() -> None:
     '''
     Displays available options for taylor_diagram_subplot() function.
     '''
     _disp('General options:')


     _dispopt("'alpha'","Blending of symbol face color (0.0 transparent through 1.0 opaque)" +
              "\n\t\t" + "(Default: 1.0)")

     _dispopt("'axisMax'",'Maximum for the radial contours')

     _dispopt("'colFrame'", "Color for both the y (left) and x (bottom) spines. "+
                            "(Default: '#000000' (black))")

     _dispopt("'colorMap'","'on'/ 'off' (default): "  + 
         "Switch to map color shading of markers to colormap ('on')\n\t\t"  +
         "or min to max range of RMSDz values ('off').")

     _dispopt("'labelWeight'","weight of the x & y axis labels")

     _dispopt("'numberPanels'",'1 or 2: Panels to display (1 for ' +
              'positive correlations, 2 for positive and negative' +
              ' correlations). \n\t\tDefault value depends on ' +
              'correlations (CORs)')

     _dispopt("'overlay'","'on' / 'off' (default): " +
         'Switch to overlay current statistics on Taylor diagram. ' +
         '\n\t\tOnly markers will be displayed.')

     _disp("OPTIONS when 'colormap' == 'on'")
     _dispopt("'cmap'","Choice of colormap. (Default: 'jet')")
     _dispopt("'cmap_marker'","Marker to use with colormap (Default: 'd')")
     _dispopt("'cmap_vmax'","Maximum range of colormap (Default: None)")
     _dispopt("'cmap_vmin'","Minimum range of colormap (Default: None)")
     _disp('')

     _disp('Marker options:')

     _dispopt("'MarkerDisplayed'",
         "'marker' (default): Experiments are represented by individual " + 
         "symbols\n\t\t"  + 
         "'colorBar': Experiments are represented by a color described " + \
         "in a colorbar")

     _disp("OPTIONS when 'MarkerDisplayed' == 'marker'")

     _dispopt("'markerColor'",'Single color to use for all markers'  +
         ' (Default: red)')

     _dispopt("'markerColors'", "Dictionary with up to two colors as keys ('face', 'edge') " +
              "to use for all markers " + 
              "\n\t\twhen 'markerlegend' == 'off' or None." +
              "\n\t\tIf None or 'markerlegend' == 'on', then uses only the " +
              "value of 'markercolor'. (Default: None)")

     _dispopt("'markerLabel'",'Labels for markers')

     _dispopt("'markerLabelColor'",'Marker label color (Default: black)')

     _dispopt("'markerLegend'","'on' / 'off' (default): "  +
         'Use legend for markers')

     _dispopt("'markers'",'Dictionary providing individual control of the marker ' +
              'label, label color, symbol, size, face color, and edge color'  +
         ' (Default: none)')

     _dispopt("'markerSize'",'Marker size (Default: 10)')

     _dispopt("'markerSymbol'","Marker symbol (Default: '.')")

     _disp("OPTIONS when MarkerDisplayed' == 'colorbar'")

     _dispopt("'cmapzdata'","Data values to use for color mapping of markers, " + 
              "e.g. RMSD or BIAS." +
              "\n\t\t(Used to make range of RMSDs values appear above color bar.)")
     
     _dispopt("'locationColorBar'","Location for the colorbar, 'NorthOutside' " +
             "or 'EastOutside'")

     _dispopt("'titleColorBar'",'Title of the colorbar.')

     _disp('')

     _disp('RMS axis options:')

     _dispopt("'colRMS'",'Color for RMS labels (Default: medium green)')

     _dispopt("'labelRMS'","RMS axis label (Default 'RMSD')")

     _dispopt("'rincRMS'",'Axis tick increment for RMS values')

     _dispopt("'rmsLabelFormat'","String format for RMS contour labels, e.g. '0:.2f'.\n\t\t" +
              "(Default '0', format as specified by str function.)")

     _dispopt("'showlabelsRMS'","'on' (default) / 'off': "  +
         'Show the RMS tick labels')

     _dispopt("'styleRMS'",'Line style of the RMS grid')

     _dispopt("'tickRMS'",'RMS values to plot grid circles from ' +
              'observation point')

     _dispopt("'tickRMSangle'",'Angle for RMS tick labels with the ' +
              'observation point. Default: 135 deg.')

     _dispopt("'titleRMS'","'on' (default) / 'off': "  +
         'Show RMSD axis title')

     _dispopt("'titleRMSDangle'","angle at which to display the 'RMSD' label for the\n\t\t" +
              "RMSD contours (Default: 160 degrees)")

     _dispopt("'widthRMS'",'Line width of the RMS grid')
     _disp('')

     _disp('STD axis options:')

     _dispopt("'colSTD'",'STD grid and tick labels color. (Default: black)')

     _dispopt("'colsSTD'", "STD dictionary of grid colors with: " +
         "'grid', 'tick_labels', 'title' keys/values." +
         "\n\t\tIf not provided or None, considers the monotonic 'colSTD' argument. " + 
         "(Default: None")  # subplot-specific

     _dispopt("'rincSTD'",'axis tick increment for STD values')

     _dispopt("'showlabelsSTD'","'on' (default) / 'off': "  +
         'Show the STD tick labels')

     _dispopt("'styleSTD'",'Line style of the STD grid')

     _dispopt("'tickSTD'",'STD values to plot gridding circles from ' + 
              'origin')

     _dispopt("'titleSTD'","'on' (default) / 'off': "  +
         'Show STD axis title')

     _dispopt("'widthSTD'",'Line width of the STD grid')
     _disp('')

     _disp('CORRELATION axis options:')

     _dispopt("'colCOR'", 'CORRELATION grid color. Default: blue')

     _dispopt("'colsCOR'", "CORRELATION dictionary of grid colors with: " +
         "'grid', 'tick_labels', 'title' keys/values." + 
         "\n\t\tIf not provided or None, considers the monotonic 'colCOR' argument." +
         "Default: None")  # subplot-specific

     _dispopt("'showlabelsCOR'","'on' (default) / 'off': "  +
         'Show the CORRELATION tick labels')

     _dispopt("'styleCOR'",'Line style of the CORRELATION grid')

     _dispopt("'tickCOR[panel]'","Tick values for correlation coefficients for " +
              "two types of panels")

     _dispopt("'titleCOR'","'on' (default) / 'off': "  +
         'Show CORRELATION axis title')

     _dispopt("'titleCORshape'", "The shape of the label 'correlation coefficient'. " +
                                 "\n\t\tAccepted values are 'curved' or 'linear' " +
                                 "(Default: 'curved'),")

     _dispopt("'widthCOR'",'Line width of the COR grid')
     _disp('')

     _disp('Observation Point options:')

     _dispopt("'colObs'","Observation STD color. (Default: magenta)")

     _dispopt("'markerObs'","Marker to use for x-axis indicating observed STD." +
              "\n\t\tA choice of 'None' will suppress appearance of marker. (Default None)")

     _dispopt("'styleObs'","Line style for observation grid line. A choice of empty string ('')\n\t\t" +
              "will suppress appearance of the grid line. (Default: '')")

     _dispopt("'titleOBS'","Label for observation point (Default: '')")

     _dispopt("'widthOBS'",'Line width for observation grid line')

     _disp('')

     _disp('CONTROL options:')

     _dispopt("'checkStats'","'on' / 'off' (default): "  +
         'Check input statistics satisfy Taylor relationship')

     _disp('Plotting Options from File:')

     _dispopt("'taylor_options_file'","name of CSV file containing values for optional " +
            "arguments" +
            "\n\t\t" + "of the taylor_diagram function. If no file suffix is given," +
            "\n\t\t" + "a '.csv' is assumed. (Default: empty string '')")

def _disp(text):
     print(text)

def _dispopt(optname, optval):
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

def _get_taylor_diagram_arguments(*args):
    '''
    Get arguments for taylor_diagram function.
     
    Retrieves the arguments supplied to the TAYLOR_DIAGRAM function as
    arguments and displays the optional arguments if none are supplied.
    Otherwise, tests the first 3 arguments are numeric quantities and 
    returns their values.
     
    INPUTS:
    args: variable-length input argument list with size 4
     
    OUTPUTS:
    CAX: Subplot axes 
    STDs: Standard deviations
    RMSs: Centered Root Mean Square Difference 
    CORs: Correlation
    '''

     # Check amount of values provided and display options list if needed
    import numbers
    
    nargin = len(args)
    if nargin == 0:
        # Display options list
        _display_taylor_diagram_options()
        return [], [], [], []
    elif nargin == 3:
        stds, rmss, cors = args
        CAX = plt.gca()
    elif nargin == 4:
        CAX, stds, rmss, cors = args
        if not hasattr(CAX, 'axes'):
            raise ValueError('First argument must be a matplotlib axes.')
    else:
        raise ValueError('Must supply 3 or 4 arguments.')
    del nargin
    
    # Check data validity
    STDs = _ensure_np_array_or_die(stds, "STDs")
    RMSs = _ensure_np_array_or_die(rmss, "RMSs")
    CORs = _ensure_np_array_or_die(cors, "CORs")
    
    return CAX, STDs, RMSs, CORs

def taylor_diagram(*args, **kwargs) -> None:
     '''
    Plot a Taylor diagram from statistics of different series.
    
    taylor_diagram(STDs,RMSs,CORs,keyword=value)
    
    The first 3 arguments must be the inputs as described below followed by
    keywords in the format OPTION = value. An example call to the function 
    would be:
    
    taylor_diagram(STDs,RMSs,CORs,markerdisplayed='marker')
    
    INPUTS:
    STDs: Standard deviations
    RMSs: Centered Root Mean Square Difference 
    CORs: Correlation
    
    Each of these inputs are one-dimensional with the same length. First
    index corresponds to the reference series for the diagram. For 
    example STDs[1] is the standard deviation of the reference series 
    and STDs[2:N] are the standard deviations of the other series. Note 
    that only the latter are plotted.
 
    Note that by definition the following relation must be true for all 
    series i:

     RMSs(i) = sqrt(STDs(i).^2 + STDs(1)^2 - 2*STDs(i)*STDs(1).*CORs(i))

    This relation is checked if the checkStats option is used, and if not 
    verified an error message is sent. This relation is not checked by
    default. Please see Taylor's JGR article for more informations about 
    this relation.
   
    OUTPUTS:
    None.
    
    LIST OF OPTIONS:
    For an exhaustive list of options to customize your diagram, call the 
    function without arguments at a Python command line:
    % python
    >>> import skill_metrics as sm
    >>> sm.taylor_diagram()
    
    Reference:
 
    Taylor, K. E. (2001), Summarizing multiple aspects of model 
      performance in a single diagram, J. Geophys. Res., 106(D7),
      7183-7192, doi:10.1029/2000JD900719.
    
    Author: Peter A. Rochford
            rochford.peter1@gmail.com

    Created on Dec 3, 2016
    Revised on Aug 23, 2022
     '''

     # Check for no arguments
     if len(args) == 0: return

     # Process arguments (if given)
     ax, STDs, RMSs, CORs = _get_taylor_diagram_arguments(*args)

     # Get options
     options = get_taylor_diagram_options(CORs, **kwargs)

     # Check the input statistics if requested.
     check_taylor_stats(STDs, RMSs, CORs, 0.01) if options['checkstats'] == 'on' else None

     # Express statistics in polar coordinates.
     rho, theta = STDs, np.arccos(CORs)

     #  Get axis values for plot
     axes = get_taylor_diagram_axes(ax, rho, options)

     if options['overlay'] == 'off':
         # Draw circles about origin
         overlay_taylor_diagram_circles(ax, axes, options)

         # Draw lines emanating from origin
         overlay_taylor_diagram_lines(ax, axes, options)

         # Plot axes for Taylor diagram
         axes_handles = plot_taylor_axes(ax, axes, options)

         # Plot marker on axis indicating observation STD
         plot_taylor_obs(ax, axes_handles, STDs[0], axes, options)

         del axes_handles

     # Plot data points. Note that only rho[1:N] and theta[1:N] are 
     # plotted.
     X = np.multiply(rho[1:], np.cos(theta[1:]))
     Y = np.multiply(rho[1:], np.sin(theta[1:]))

     # Plot data points
     lowcase = options['markerdisplayed'].lower()
     if lowcase == 'marker':
         plot_pattern_diagram_markers(ax, X, Y, options)
     elif lowcase == 'colorbar':
         nZdata = len(options['cmapzdata'])
         if nZdata == 0:
             # Use Centered Root Mean Square Difference for colors
             plot_pattern_diagram_colorbar(ax, X, Y, RMSs[1:], options)
         else:
             # Use Bias values for colors
             plot_pattern_diagram_colorbar(ax, X, Y, options['cmapzdata'][1:], options)
     else:
         raise ValueError('Unrecognized option: ' + 
                          options['markerdisplayed'])

     return None
