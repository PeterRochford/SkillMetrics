import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings

def add_legend(markerLabel, option, rgba, markerSize, fontSize, hp = []):
    '''
    Adds a legend to a pattern diagram.
    
    Adds a legend to a plot according to the data type containing the 
    provided labels. If labels are provided as a list they will appear 
    in the legend beside the marker provided in the list of handles in 
    a one-to-one match. If labels are provided as a dictionary they will 
    appear beside a dot with the color value given to the label.
    
    INPUTS:
    markerLabel : list or dict variable containing markers and labels to
                  appear in legend
                  
                  A list variable must have the format:
                  markerLabel = ['M1', 'M2', 'M3']
                  
                  A dictionary variable must have the format:
                  markerLabel = = {'ERA-5': 'r', 'TRMM': 'b'}
                  where each key is the label and each value the color for 
                  the marker
    
    hp : list of plot handles that match markerLabel when latter is a list
    option : dictionary containing option values. (Refer to 
        GET_TARGET_DIAGRAM_OPTIONS function for more information.)
    option['numberpanels'] : Number of panels to display
                             = 1 for positive correlations
                             = 2 for positive and negative correlations
    rgba : a 4-tuple where the respective tuple components represent red, 
           green, blue, and alpha (opacity) values for a color
    markerSize : point size of markers
    fontSize : font size in points of labels
    
    OUTPUTS:
    None

    Created on Mar 2, 2019
    Revised on Mar 2, 2019
    
    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com
    '''

    if type(markerLabel) is list:
        
        # Check for empty list of plot handles
        if len(hp) == 0:
            raise ValueError('Empty list of plot handles')
        elif len(hp) != len(markerLabel):
            raise ValueError('Number of labels and plot handle do not match: ' +
                             str(len(markerLabel)) + ' != ' + str(len(hp)))
        
        # Add legend using labels provided as list
        if len(markerLabel) <= 6:
            # Put legend in a default location
            markerlabel = tuple(markerLabel)
            plt.legend(hp, markerlabel, loc = 'upper right',
                                 fontsize = fontSize, numpoints=1,
                                 bbox_to_anchor=(1.2,1.0))
        else:
            # Put legend to right of the plot in multiple columns as needed

            nmarkers = len(markerLabel)
            ncol = int(math.ceil(nmarkers / 15.0))
            markerlabel = tuple(markerLabel)

            # Shift figure to include legend
            plt.gcf().subplots_adjust(right=0.6)

            # Plot legend of multi-column markers
            # Note: do not use bbox_to_anchor as this cuts off the legend
            plt.legend(hp, markerlabel, loc = (1.1, 0.25),
                        fontsize = fontSize, numpoints=1, ncol = ncol)

    elif type(markerLabel) is dict:
        
        # Add legend using labels provided as dictionary
            
        # Define legend elements
        legend_elements = []
        for key, value in markerLabel.items():
            legend_object = Line2D([0], [0], marker='.', markersize = markerSize,
                 markerfacecolor = rgba, markeredgecolor = value, label=key, linestyle='')
            legend_elements.append(legend_object)

        # Put legend in a default location
        plt.legend(handles=legend_elements, loc = 'upper right',
                             fontsize = fontSize, numpoints=1,
                             bbox_to_anchor=(1.2,1.0))

        if _checkKey(option, 'numberpanels') and option['numberpanels'] == 2:
            # add padding so legend is not cut off
            plt.tight_layout(pad=1)
    else:
        raise Exception('markerLabel type is not a list or dictionary: ' + 
                        str(type(markerLabel)))
    
def _checkKey(dictionary, key): 
    if key in dictionary.keys(): 
        return True
    else: 
        return False 
