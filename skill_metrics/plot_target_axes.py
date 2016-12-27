import matplotlib.pyplot as plt
import numpy as np

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
    '''
    
    xtick = axes['xtick']
    ytick = axes['ytick']
    
    # Draw axis lines
    plt.plot([xtick[0], xtick[-1]], [0, 0], 'k')  # x-axis
    plt.hold(True)
    plt.plot([0, 0], [ytick[0], ytick[-1]], 'k')  # y-axis
    
    # Get offsets
    gca = plt.gca()
    Xoff = np.diff(gca.get_xlim())[0] / 40
    Yoff = np.diff(gca.get_ylim())[0] / 40
    
    # Plot new ticks with labels
    y = -2.*Yoff
    for i, x in enumerate(xtick):
        plt.plot([x, x], [0, Yoff], '-k')
        plt.text(x, y, axes['xlabel'][i], horizontalalignment='center')

    x = -1.*Xoff
    for i, y in enumerate(ytick):
        if i > 0:
            plt.plot([Xoff, 0], [y, y], '-k')
        else:
            plt.plot([Xoff, 0], [y - 0.01 * Yoff, y - 0.01 * Yoff], '-k')
            
        plt.text(x, y - 0.5 * Yoff, axes['ylabel'][i], horizontalalignment='right')

    # Label x-axis with text at end of axis
    xpos = xtick[-1] + 3 * xtick[-1] / 30;  ypos = 0
    plt.text(xpos, ypos, 'uRMSD', color='k', horizontalalignment='left')
    
    # Label y-axis with text at end of axis
    xpos = 0;  ypos = ytick[-1] + 3 * ytick[-1] / 30
    plt.text(xpos, ypos, 'Bias', color='k', horizontalalignment='center')
    
    plt.setp(gca, frame_on=False)
    plt.axis('equal')
    plt.axis('off')
    plt.gcf().patch.set_facecolor('w')
