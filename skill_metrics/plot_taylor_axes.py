import matplotlib.pyplot as plt
import numpy as np

def plot_taylor_axes(axes, cax, option):
    '''
    Plot axes for taylor diagram.
    
    Plots the x & y axes for a Taylor diagram using the information 
    provided in the AXES dictionary returned by the 
    GET_TAYLOR_DIAGRAM_AXES function.
    
    INPUTS:
    axes   : data structure containing axes information for target diagram
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
    option['titlestd']     : title fot STD axis
 
    OUTPUTS:
    ax: returns a list of handles of axis labels
    
    Author: Peter A. Rochford
    Acorn Science & Innovation
    prochford@acornsi.com

    Created on Dec 3, 2016

    @author: rochfordp  
    '''
    
    ax = []
    axlabweight = 'bold' 
    if option['numberpanels'] == 1:
        # Single panel
        
        if option['titlestd'] == 'on':
            ttt = plt.ylabel('test', fontsize = 14);
            x = -0.15*axes['rmax']; y = 0.7*axes['rmax'];
            handle = plt.text(x,y,'Standard Deviation', rotation = 90, 
                              color = option['colstd'], 
                              fontweight = axlabweight, 
                              fontsize = plt.get(ttt,'fontsize'),
                              horizontalalignment = 'center')
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
                            fontsize = plt.get(ax[0],'fontsize'),
                            fontweight = axlabweight)
                ax.append(handle) 
        
        if option['titlerms'] == 'on':
            pos1 = option['tickrmsangle']+(180-option['tickrmsangle'])/2; 
            DA = 15; pos1 = 160;
            lab = 'RMSD' 
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            if option['tickrms'][0] > 0:
                dd = 0.7*option['tickrms'][0] + 0.3*option['tickrms'][1]
            else:
                dd = 0.7*option['tickrms'][1] + 0.3*option['tickrms'][2]
            for ii,ith in enumerate(c):
                xtextpos = axes['dx'] + dd*np.cos(ith*np.pi/180) 
                ytextpos = dd*np.sin(ith*np.pi/180) 
                handle = plt.text(xtextpos,ytextpos,lab[ii])
                handle.set(rotation = ith-90, color = option['colrms'], 
                    horizontalalignment = 'center', 
                    verticalalignment = 'top', 
                    fontsize = plt.get(ax[0],'fontsize'),
                    fontweight = axlabweight)
                ax.append(handle)
        
    else:
        # Double panel
    
        if option['titlestd'] == 'on':
            ttt = plt.ylabel('test', fontsize = 14);
            x = 0; y = -0.15*axes['rmax'];
            handle = plt.text(x,y,'Standard Deviation', rotation = 0, 
                              color = option['colstd'], 
                              fontweight = axlabweight, 
                              fontsize = plt.get(ttt,'fontsize'),
                              horizontalalignment = 'center')
            ax.append(handle)

        if option['titlecor'] == 'on':
            pos1 = 90; DA = 25;
            lab = 'Correlation Coefficient' 
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            dd = 1.1*axes['rmax']
            for ii,ith in enumerate(c):
                handle = plt.text(dd*np.cos(ith*np.pi/180),
                                  dd*np.sin(ith*np.pi/180),lab[ii])
                handle.set(rotation = ith-90, color = option['colcor'],
                    horizontalalignment = 'center', 
                    verticalalignment = 'bottom', 
                    fontsize = plt.get(ax[0],'fontsize'),
                    fontweight = axlabweight) 
                ax.append(handle) 
        
        if option['titlerms'] == 'on':
            pos1 = 160; DA = 10;
            lab = 'RMSD' 
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            dd = 1.05*option['tickrms'][0]
            for ii,ith in enumerate(c):
                xtextpos = axes['dx'] + dd*np.cos(ith*np.pi/180) 
                ytextpos = dd*np.sin(ith*np.pi/180) 
                handle = plt.text(xtextpos,ytextpos,lab[ii])
                handle.set(rotation = ith-90, color = option['colrms'],
                    horizontalalignment = 'center', 
                    verticalalignment = 'bottom',
                    fontsize = plt.get(ax[0],'fontsize'),
                    fontweight = axlabweight)
                ax.append(handle)
    
    # VARIOUS ADJUSTMENTS TO THE PLOT:
    cax.set_aspect('equal')
    plt.axis('off')
    plt.gcf().patch.set_facecolor('w')

    # set axis limits
    if option['numberpanels'] == 2:
        axislim = [axes['rmax']*x for x in [-1.15, 1.15, 0, 1.15]]
        plt.axis(axislim) 
        plt.plot([-axes['rmax'], axes['rmax']],[0, 0],
                 color = axes['tc'], linewidth = 2)
        plt.plot([0, 0],[0, axes['rmax']], color = axes['tc'])
    else:
        axislim = [axes['rmax']*x for x in [0, 1.15, 0, 1.15]]
        plt.axis(axislim) 
        plt.plot([0, axes['rmax']],[0, 0], color = axes['tc'], 
                 linewidth = 2) 
        plt.plot([0, 0],[0, axes['rmax']], color = axes['tc'], 
                 linewidth = 2) 
