from matplotlib import rcParams
from skill_metrics.get_axis_tick_label import get_axis_tick_label
from skill_metrics import get_from_dict_or_default
import matplotlib
import numpy as np

def plot_taylor_axes(ax: matplotlib.axes.Axes, axes: dict, option: dict) \
        -> list:
    '''
    Plot axes for Taylor diagram.
    
    Plots the x & y axes for a Taylor diagram using the information 
    provided in the AXES dictionary returned by the 
    GET_TAYLOR_DIAGRAM_AXES function.

    INPUTS:
    ax     : matplotlib.axes.Axes object in which the Taylor diagram will be plotted
    axes   : data structure containing axes information for Taylor diagram
    option : data structure containing option values. (Refer to 
             GET_TAYLOR_DIAGRAM_OPTIONS function for more information.)
    option['colcor']        : CORs grid and tick labels color (Default: blue)
    option['colscor']       : dictionary with two possible colors as keys ('grid',
                                'tick_labels') or None, if None then considers only the
                                value of 'colscor' (Default: None)
    option['colrms']        : RMS grid and tick labels color (Default: green)
    option['colstd']        : STD grid and tick labels color (Default: black)
    option['colsstd']       : dictionary with two possible colors keys ('ticks',
                                'tick_labels') or None, if None then considers only the
                                value of 'colsstd' (Default: None)
    option['labelrms']      : RMS axis label, e.g. 'RMSD'
    option['numberpanels']  : number of panels (quadrants) to use for Taylor
                                diagram
    option['tickrms']       : RMS values to plot gridding circles from
                                observation point
    option['titlecor']      : title for CORRELATION axis
    option['titlerms']      : title for RMS axis
    option['titlestd']      : title for STD axis
    option['titlecorshape'] : defines the shape of the label "correlation coefficient"
                                as either 'curved' or 'linear' (Default: 'curved')
 
    OUTPUTS:
    ax: returns a list of handles of axis labels
    
    Authors:
    Peter A. Rochford
    rochford.peter1@gmail.com

    Andre D. L. Zanchetta (adapting Peter A. Rochford's code)
        adlzanchetta@gmail.com

    Created on Dec 3, 2016
    Revised on Aug 14, 2022
    '''
    
    axes_handles = []
    axlabweight = option['labelweight']
    fontSize = rcParams.get('font.size') + 2
    lineWidth = rcParams.get('lines.linewidth')
    fontFamily = rcParams.get('font.family')

    if option['numberpanels'] == 1:
        # Single panel
        
        if option['titlestd'] == 'on':
            color = get_from_dict_or_default(
                option, 'colstd', 'colsstd', 'title')
            handle = ax.set_ylabel('Standard Deviation',
                                   color=color,
                                   fontweight=axlabweight,
                                   fontsize=fontSize,
                                   fontfamily=fontFamily)
            axes_handles.append(handle)
            del color, handle

        # plot correlation title
        if option['titlecor'] == 'on':
            color = get_from_dict_or_default(
                option, 'colcor', 'colscor', 'title')
            pos1 = 45
            lab = 'Correlation Coefficient'

            if option['titlecorshape'] == 'curved':
                DA  = 15
                c = np.fliplr([np.linspace(pos1-DA, pos1+DA, len(lab))])[0]
                dd = 1.1 * axes['rmax']
                for ii, ith in enumerate(c):
                    cur_x = dd*np.cos(ith*np.pi/180)
                    cur_y = dd*np.sin(ith*np.pi/180)
                    # print("%s: %.03f, %.03f, %.03f" % (lab[ii], cur_x, cur_y, ith))
                    handle = ax.text(dd*np.cos(ith*np.pi/180),
                                    dd*np.sin(ith*np.pi/180),
                                    lab[ii])
                    handle.set(rotation=ith-90,
                            color=color,
                            horizontalalignment='center',
                            verticalalignment='bottom',
                            fontsize=fontSize,
                            fontfamily=fontFamily,
                            fontweight=axlabweight)
                    axes_handles.append(handle)
                    del ii, ith, handle
                del DA, c, dd

            elif option['titlecorshape'] == 'linear':
                pos_x_y = 1.13 * axes['rmax'] * np.cos(pos1*np.pi/180)
                handle = ax.text(pos_x_y, pos_x_y, "Correlation Coefficient")
                handle.set(rotation=-45,
                           color=color,
                           horizontalalignment='center',
                           verticalalignment='center',
                           fontsize=fontSize,
                           fontfamily=fontFamily,
                           fontweight=axlabweight)
                del pos_x_y, handle

            else:
                raise ValueError("Invalid value for 'titlecorshape': %s" %
                                 option['titlecorshape'])

            del color, pos1, lab
        
        if option['titlerms'] == 'on':
            lab = option['labelrms']
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
                handle = ax.text(xtextpos,ytextpos,lab[ii])
                handle.set(rotation = ith-90, color = option['colrms'], 
                    horizontalalignment = 'center', 
                    verticalalignment = 'top', 
                    fontsize = fontSize, fontweight = axlabweight)
                axes_handles.append(handle)
        
    else:
        # Double panel
    
        if option['titlestd'] == 'on':
            color = get_from_dict_or_default(
                option, 'colstd', 'colsstd', 'title')
            handle = ax.set_xlabel('Standard Deviation',
                                   color = color,
                                   fontweight = axlabweight,
                                   fontsize = fontSize)

            axes_handles.append(handle)
            del color, handle

        if option['titlecor'] == 'on':
            color = get_from_dict_or_default(
                option, 'colcor', 'colscor', 'title')
            pos1 = 90; DA = 25;
            lab = 'Correlation Coefficient' 
            c = np.fliplr([np.linspace(pos1-DA,pos1+DA,len(lab))])[0]
            dd = 1.1*axes['rmax']

            # Write label in a circular arc
            for ii, ith in enumerate(c):
                handle = ax.text(dd*np.cos(ith*np.pi/180),
                                  dd*np.sin(ith*np.pi/180),lab[ii])
                handle.set(rotation = ith-90, color = color,
                    horizontalalignment = 'center', 
                    verticalalignment = 'bottom', 
                    fontsize = fontSize,
                    fontweight = axlabweight)
                axes_handles.append(handle)

                del ii, ith, handle
            del color, pos1, DA, lab, c, dd
        
        if option['titlerms'] == 'on':
            lab = option['labelrms']
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
                handle = ax.text(xtextpos,ytextpos,lab[ii])
                handle.set(rotation = ith-90, color = option['colrms'],
                    horizontalalignment = 'center', 
                    verticalalignment = 'bottom',
                    fontsize = fontSize,
                    fontweight = axlabweight)
                axes_handles.append(handle)
    
    #  Set color of tick labels to that specified for STD contours
    labels_color = get_from_dict_or_default(option, 'colstd', 'colsstd', 'tick_labels')
    ticks_color = get_from_dict_or_default(option, 'colstd', 'colsstd', 'ticks')
    ax.tick_params(axis='both', color=ticks_color, labelcolor=labels_color)
    del labels_color, ticks_color

    # VARIOUS ADJUSTMENTS TO THE PLOT:
    ax.set_aspect('equal')
    ax.set_frame_on(None)

    # set axes limits, set ticks, and draw axes lines
    ylabel = [];
    if option['numberpanels'] == 2:
        xtick = [-option['tickstd'], option['tickstd']]
        if 0 in option['tickstd']:
            xtick = np.concatenate((-option['tickstd'][1:], option['tickstd']), axis=None)
        else:
            xtick = np.concatenate((-option['tickstd'][0:], 0, option['tickstd']), axis=None)
        xtick = np.sort(xtick)
        
        # Set x tick labels
        xlabel = [];
        for i in range(len(xtick)):
            if xtick[i] == 0:
                label = '0'
            else:
                label = get_axis_tick_label(abs(xtick[i]))
            xlabel.append(label)

        ax.set_xticks(xtick)
        ax.set_xticklabels(xlabel, fontfamily=fontFamily)

        axislim = [axes['rmax']*x for x in [-1, 1, 0, 1]]
        ax.set_xlim(axislim[0:2])
        ax.set_ylim(axislim[2:])
        ax.plot([-axes['rmax'], axes['rmax']],[0, 0],
                 color = axes['tc'], linewidth = lineWidth+1)
        ax.plot([0, 0],[0, axes['rmax']], color = axes['tc'])

        # hide y-axis line
        ax.axes.get_yaxis().set_visible(False)
    else:
        ytick = ax.get_yticks()
        ytick = list(filter(lambda x: x >= 0 and x <= axes['rmax'], ytick))
        axislim = [axes['rmax']*x for x in [0, 1, 0, 1]]
        ax.set_xlim(axislim[0:2])
        ax.set_ylim(axislim[2:])
        
        # Set y tick labels
        for i in range(len(ytick)):
            label = get_axis_tick_label(ytick[i])
            ylabel.append(label)

        ax.set_xticks(ytick)
        ax.set_yticks(ytick)
        ax.set_xticklabels(ylabel, fontfamily=fontFamily, fontsize=fontSize*0.9)
        ax.set_yticklabels(ylabel, fontfamily=fontFamily, fontsize=fontSize*0.9)

        ax.plot([0,
                 axes['rmax']],[0, 0],
                 color = axes['tc'],
                 linewidth = lineWidth+2)
        ax.plot([0, 0],
                [0, axes['rmax']],
                 color = axes['tc'],
                 linewidth = lineWidth+1)

    return axes_handles
