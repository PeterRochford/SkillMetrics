import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

def plot_taylor_axes(axes, cax, option):
    '''
    Plot axes for Taylor diagram.
    
    Plots the x & y axes for a Taylor diagram using the information 
    provided in the AXES dictionary returned by the 
    GET_TAYLOR_DIAGRAM_AXES function.
    
    INPUTS:
    axes   : data structure containing axes information for Taylor diagram
    cax    : handle for plot axes
    option : data structure containing option values. (Refer to 
             GET_TAYLOR_DIAGRAM_OPTIONS function for more information.)
    option['colcor']       : CORs grid and tick labels color (Default: blue)
    option['colrms']       : RMS grid and tick labels color (Default: green)
    option['colstd']       : STD grid and tick labels color (Default: black)
    option['numberpanels'] : number of panels (quadrants) to use for Taylor
                          diagram
    option['tickrms']      : RMS values to plot gridding circles from 
                             observation point
    option['titlecor']     : title for CORRELATION axis
    option['titlerms']     : title for RMS axis
    option['titlestd']     : title for STD axis
 
    OUTPUTS:
    ax: returns a list of handles of axis labels
    
    Author: Peter A. Rochford
    Acorn Science & Innovation
    prochford@acornsi.com

    Created on Dec 3, 2016
    Revised on Dec 31, 2018

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''
    
    ax = []
    axlabweight = 'bold'
    fontSize = rcParams.get('font.size') + 2
    lineWidth = rcParams.get('lines.linewidth')

    if option['numberpanels'] == 1:
        # Single panel
        
        if option['titlestd'] == 'on':
            handle = plt.ylabel('Standard Deviation',
                              color = option['colstd'], 
                              fontweight = axlabweight, fontsize = fontSize)
            ax.append(handle)
        
        if option['titlecor'] == 'on':
            pos1 = 45; DA = 15;
            lab = 'Correlation Coefficient' 
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            dd = 1.1*axes['rmax']
            for ii,ith in enumerate(c): 
                handle = plt.text(dd*np.cos(ith*np.pi/180),
                                   dd*np.sin(ith*np.pi/180),
                                   lab[ii]) 
                handle.set(rotation = ith-90,color = option['colcor'],
                            horizontalalignment = 'center',
                            verticalalignment = 'bottom',
                            fontsize = fontSize, fontweight = axlabweight)
                ax.append(handle) 
        
        if option['titlerms'] == 'on':
            lab = 'RMSD'
            pos1 = option['titlermsdangle']; DA = 10
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            if option['tickrms'][0] > 0:
                dd = 0.8*option['tickrms'][0] + 0.2*option['tickrms'][1]
            else:
                dd = 0.8*option['tickrms'][1] + 0.2*option['tickrms'][2]
            
            # Adjust spacing of label letters if on too small an arc
            posFraction = dd/axes['rmax']
            if posFraction < 0.35:
                DA = 2*DA
                c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]

            # Write label in a circular arc               
            for ii,ith in enumerate(c):
                xtextpos = axes['dx'] + dd*np.cos(ith*np.pi/180) 
                ytextpos = dd*np.sin(ith*np.pi/180) 
                handle = plt.text(xtextpos,ytextpos,lab[ii])
                handle.set(rotation = ith-90, color = option['colrms'], 
                    horizontalalignment = 'center', 
                    verticalalignment = 'top', 
                    fontsize = fontSize, fontweight = axlabweight)
                ax.append(handle)
        
    else:
        # Double panel
    
        if option['titlestd'] == 'on':
            handle = plt.xlabel('Standard Deviation',
                              color = option['colstd'], 
                              fontweight = axlabweight, fontsize = fontSize)
            ax.append(handle)

        if option['titlecor'] == 'on':
            pos1 = 90; DA = 25;
            lab = 'Correlation Coefficient' 
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            dd = 1.1*axes['rmax']

            # Write label in a circular arc
            for ii,ith in enumerate(c):
                handle = plt.text(dd*np.cos(ith*np.pi/180),
                                  dd*np.sin(ith*np.pi/180),lab[ii])
                handle.set(rotation = ith-90, color = option['colcor'],
                    horizontalalignment = 'center', 
                    verticalalignment = 'bottom', 
                    fontsize = fontSize, fontweight = axlabweight)
                ax.append(handle) 
        
        if option['titlerms'] == 'on':
            lab = 'RMSD' 
            pos1 = option['titlermsdangle']; DA = 10
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            if option['tickrms'][0] > 0:
                dd = 0.7*option['tickrms'][0] + 0.3*option['tickrms'][1]
            else:
                dd = 0.7*option['tickrms'][1] + 0.3*option['tickrms'][2]

            # Adjust spacing of label letters if on too small an arc
            posFraction = dd/axes['rmax']
            if posFraction < 0.35:
                DA = 2*DA
                c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]

            for ii,ith in enumerate(c):
                xtextpos = axes['dx'] + dd*np.cos(ith*np.pi/180) 
                ytextpos = dd*np.sin(ith*np.pi/180) 
                handle = plt.text(xtextpos,ytextpos,lab[ii])
                handle.set(rotation = ith-90, color = option['colrms'],
                    horizontalalignment = 'center', 
                    verticalalignment = 'bottom',
                    fontsize = fontSize, fontweight = axlabweight)
                ax.append(handle)
    

    #  Set color of tick labels to that specified for STD contours
    plt.gca().tick_params(axis='x', colors=option['colstd'])
    plt.gca().tick_params(axis='y', colors=option['colstd'])

    # VARIOUS ADJUSTMENTS TO THE PLOT:
    cax.set_aspect('equal')
    plt.box(on=None)

    # set axes limits, set ticks, and draw axes lines
    if option['numberpanels'] == 2:
        xtick = [-option['tickstd'], option['tickstd']]
        xtick = np.concatenate((-option['tickstd'][1:], option['tickstd']), axis=None)
        xtick = np.sort(xtick)
        plt.xticks(xtick)

        axislim = [axes['rmax']*x for x in [-1, 1, 0, 1]]
        plt.axis(axislim) 
        plt.plot([-axes['rmax'], axes['rmax']],[0, 0],
                 color = axes['tc'], linewidth = lineWidth+1)
        plt.plot([0, 0],[0, axes['rmax']], color = axes['tc'])

        # hide y-axis line
        plt.gca().axes.get_yaxis().set_visible(False)
    else:
        ytick, ylab = plt.yticks()
        ytick = list(filter(lambda x: x >= 0 and x <= axes['rmax'], ytick))
        axislim = [axes['rmax']*x for x in [0, 1, 0, 1]]
        plt.axis(axislim)
        plt.xticks(ytick); plt.yticks(ytick)

        plt.plot([0, axes['rmax']],[0, 0],
                 color = axes['tc'], linewidth = lineWidth+2)
        plt.plot([0, 0],[0, axes['rmax']],
                 color = axes['tc'], linewidth = lineWidth+1)

    return ax