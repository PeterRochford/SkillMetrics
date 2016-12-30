import matplotlib.pyplot as plt
import numpy as np

def overlay_taylor_diagram_lines(axes,cax,option):
    '''
    Overlay lines emanating from origin on a Taylor diagram.

    OVERLAY_TAYLOR_DIAGRAM_CIRCLES(AXES,CAX,OPTION)
    Plots lines emanating from origin to indicate correlation values (CORs) 
 
    INPUTS:
    axes   : data structure containing axes information for target diagram
    cax    : handle for plot axes
    option : data structure containing option values. (Refer to 
             GET_TAYLOR_DIAGRAM_OPTIONS function for more information.)
    option['colcor']   : CORs grid and tick labels color (Default: blue)
    option['showlabelscor'] : Show or not the CORRELATION tick labels
    option['stylecor'] : Linestyle of the CORs grid
    option['tickcor']  : CORs values to plot lines from origin
    option['widthcor'] : Line width of the CORs grid
 
    OUTPUTS:
    None.
    
    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Dec 3, 2016
   '''

    # DRAW CORRELATION LINES EMANATING FROM THE ORIGIN:
    npanels = option['numberpanels']
    corr = option['tickcor'][npanels-1]
    th  = np.arccos(corr)
    cst = np.cos(th); snt = np.sin(th);
    cs = np.append(-1.0*cst, cst)
    sn = np.append(-1.0*snt, snt)
    for i,val in enumerate(cs):
        plt.plot([0, axes['rmax']*cs[i]],[0, axes['rmax']*sn[i]], 
                 linestyle = option['stylecor'],
                 color = option['colcor'], linewidth = option['widthcor'])
    
    # annotate the lines by correlation coefficient
    if option['showlabelscor'] == 'on':
        rt = 1.05*axes['rmax']
        for i,cc in enumerate(corr):
            plt.text(rt*cst[i],rt*snt[i],str(cc), 
                     horizontalalignment = 'center', color = option['colcor'])
