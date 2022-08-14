import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import ScalarFormatter
import matplotlib

def plot_target_axes(axes):
    '''
    Plot axes for target diagram.
    
    Plots the x & y axes for a target diagram using the information 
    provided in the AXES dictionary returned by the 
    GET_TARGET_DIAGRAM_AXES function.
    
    INPUTS:
    axes   : dictionary containing axes information for target diagram
    
    OUTPUTS:
    None

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
	Hello
    '''
    
    class ScalarFormatterClass(ScalarFormatter):
        def _set_format(self):
            self.format = "%1.1f"
    
    class Labeloffset():
        def __init__(self,  ax, label="", axis="y"):
            self.axis = {"y":ax.yaxis, "x":ax.xaxis}[axis]
            self.label=label
            ax.callbacks.connect(axis+'lim_changed', self.update)
            ax.figure.canvas.draw()
            self.update(None)

    def update(self, lim):
        fmt = self.axis.get_major_formatter()
        self.axis.offsetText.set_visible(False)
        self.axis.set_label_text(self.label + " ("+ fmt.get_offset()+")" )
        print(fmt.get_offset())
    
    # Center axes location by moving spines of bounding box
    # Note: Center axes location not available in matplotlib
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # Make axes square
    ax.set_aspect('equal')

    # Set new ticks and tick labels
    plt.xticks(axes['xtick'],axes['xlabel'])
    plt.yticks(axes['ytick'],axes['ylabel'])
    
    # Set axes limits
    axislim = [axes['xtick'][0], axes['xtick'][-1], axes['ytick'][0], axes['ytick'][-1]]
    plt.axis(axislim)

    # Label x-axis
    fontSize = matplotlib.rcParams.get('font.size')
    xpos = axes['xtick'][-1] + 2*axes['xtick'][-1]/30
    ypos = axes['xtick'][-1]/30
    if axes['xoffset'] == 'None':        
       xlabelh = plt.xlabel('uRMSD', fontsize = fontSize, horizontalalignment = 'left')
    else:
       xlabelh = plt.xlabel('uRMSD' + '\n(' + axes['xoffset'] + ')', fontsize = fontSize, horizontalalignment = 'left')
    ax.xaxis.set_label_coords(xpos, ypos, transform=ax.transData)
    ax.tick_params(axis='x', direction='in') # have ticks above axis
    
    # Label y-axis
    xpos = 0
    ypos = axes['ytick'][-1] + 2*axes['ytick'][-1]/30
    if axes['yoffset'] == 'None':        
        ylabelh = plt.ylabel('Bias ', fontsize = fontSize, rotation=0, horizontalalignment = 'center')
    else:
        ylabelh = plt.ylabel('Bias ' + '(' + axes['yoffset'] + ')', fontsize = fontSize, rotation=0, horizontalalignment = 'center')
    #ylabelh = plt.ylabel('Bias', fontsize = fontSize, rotation=0, horizontalalignment = 'center')
    ax.yaxis.set_label_coords(xpos, ypos, transform=ax.transData)
    ax.tick_params(axis='y', direction='in') # have ticks on right side of axis
    
    # Set axes line width
    lineWidth = rcParams.get('lines.linewidth')
    ax.spines['left'].set_linewidth(lineWidth)
    ax.spines['bottom'].set_linewidth(lineWidth)
