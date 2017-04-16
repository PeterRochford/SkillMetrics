import numpy as np
from skill_metrics import get_target_diagram_axes
from skill_metrics import get_target_diagram_options
from skill_metrics import overlay_target_diagram_circles
from skill_metrics import plot_pattern_diagram_colorbar
from skill_metrics import plot_pattern_diagram_markers
from skill_metrics import plot_target_axes

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
    RMSDz : total Root-Mean-Square Difference (RMSD) or other quantities 
            (if 'nonRMSDz' == 'on'). Labeled on plot as "RMSD".
    
    OUTPUTS:
    None.
    
    LIST OF OPTIONS:
    For an exhaustive list of options to customize your diagram, call the 
    function without arguments at a Python command line:
    >> target_diagram
    
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

    # Check for number of arguments
    nargin = len(args)
    Bs, RMSDs, RMSDz = _get_target_diagram_arguments(*args)
    if nargin == 0: return

    # Get options
    option = get_target_diagram_options(**kwargs)

    #  Get axis values for plot
    axes = get_target_diagram_axes(RMSDs,Bs,option)
    
    # Plot axes for target diagram
    if option['overlay'] == 'off': plot_target_axes(axes)
    
    # __ Overlay circles
    overlay_target_diagram_circles(option)

    # Plot data points
    lowcase = option['markerdisplayed'].lower()
    if lowcase == 'marker':
        plot_pattern_diagram_markers(RMSDs,Bs,option)
    elif lowcase == 'colorbar':
        plot_pattern_diagram_colorbar(RMSDs,Bs,RMSDz,option)
    else:
        raise ValueError('Unrecognized option: ' + 
                         option['markerdisplayed'])

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
    RMSDz : total Root-Mean-Square Difference (RMSD) or other quantities 
            (if 'nonRMSDz' == 'on'). Labeled on plot as "RMSD".
    '''
    
    import numbers
    
    Bs=[]; RMSDs=[]; RMSDz=[];
    nargin = len(args)
    if nargin == 0:
        # Display options list
        _display_target_diagram_options()
        return Bs, RMSDs, RMSDz
    elif nargin != 3:
        raise ValueError('Must supply 3 arguments.')

    Bs = args[0]
    RMSDs = args[1]
    RMSDz = args[2]

    # Test the above are numeric quantities
    if isinstance(Bs, numbers.Number):
        Bs = np.array(Bs,ndmin=1)
    if not isinstance(Bs, np.ndarray):
        raise ValueError('Argument Bs is not a numeric array')

    if isinstance(RMSDs, numbers.Number):
        RMSDs = np.array(RMSDs,ndmin=1)
    if not isinstance(RMSDs, np.ndarray):
        raise ValueError('Argument RMSDs is not a numeric array')
 
    if isinstance(RMSDz, numbers.Number):
        RMSDz = np.array(RMSDz,ndmin=1)
    if not isinstance(RMSDz, np.ndarray):
        raise ValueError('Argument RMSDz is not a numeric array')

    return Bs, RMSDs, RMSDz

def _display_target_diagram_options():
    '''
    Displays available options for TARGET_DIAGRAM function.
    '''

    _disp('General options:')
    _dispopt("'overlay'","'on' / 'off' (default): " + 
            'Switch to overlay current statistics on target diagram. ' +
            '\n\t\tOnly markers will be displayed.')
    
    _disp('Marker options:')
    _dispopt("'MarkerDisplayed'", 
        "'marker' (default): Experiments are represented by individual symbols\n\t\t" +
        "'colorBar': Experiments are represented by a color described " + 
        'in a colorbar')
    _disp("OPTIONS when 'MarkerDisplayed' == 'marker'")
    _dispopt("'markerLabel'",'Labels for markers')
    _dispopt("'markerLabelColor'",'Marker label color (Default: black)')
    _dispopt("'markerColor'",'Marker color')
    _dispopt("'markerLegend'","'on' / 'off' (default): Use legend for markers'")
    _disp("OPTIONS when 'MarkerDisplayed' == 'colorbar'")
    _dispopt("'nonRMSDs'","'on'/ 'off' (default): " + 
            'Values in RMSDs do not correspond to total RMS Differences.\n\t\t' +
            '(Used to make range of RMSDs values appear above color bar.)')
    _dispopt("'titleColorBar'",'Title of the colorbar.')
     
    _disp('Axes options:')
    _dispopt("'ticks'",'define tick positions ' +
            '(default is that used by axis function)')
    _dispopt("'xtickLabelPos'",'position of the tick labels ' +
            'along the x-axis (empty by default)')
    _dispopt("'ytickLabelPos'",'position of the tick labels ' +
            'along the y-axis (empty by default)')
    _dispopt("'equalAxes'","'on' (default) / 'off': Set axes to be equal")
    _dispopt("'limitAxis'",'Max for the Bias & uRMSD axis')
     
    _disp('Diagram options:')
    _dispopt("'circles'",'define the radii of circles to draw ' +
            '(default of (maximum RMSDs)*[.7 1], [.7 1] when normalized diagram)')
    _dispopt("'circleLineSpec'",'Circle line specification (default ' +
            "dashed black, '--k')")
    _dispopt("'circleLineWidth'",'Circle line width')
    _dispopt("'obsUncertainty'",'Observational Uncertainty (default of 0)')
    _dispopt("'normalized'","'on' / 'off' (default): normalized target diagram")

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
