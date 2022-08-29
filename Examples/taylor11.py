'''
How to create a Taylor diagram with a color bar showing bias

An eleventh example of how to create a Taylor diagram given one set of
reference observations and multiple model predictions for the quantity.

This example is a variation on the sixth example (taylor6) where now the
markers are displayed in a color spectrum corresponding to their BIAS. A
color bar is automatically displayed showing the correspondence with the
BIAS values.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python taylor11.py -nosave

All functions in the Skill Metrics library are designed to only work with
one-dimensional arrays, e.g. time series of observations at a selected
location. The one-dimensional data are stored in arrays named: sdev, crmsd, 
ccoef, and bias. Each of these contain 1 reference value (first position) 
and 4 prediction values, for a total of 5 values. The plot is written to 
a file in Portable Network Graphics (PNG) format.

This data was provide courtesy of Mostafa Khoshchehreh.

Authors: Peter A. Rochford
         Andre D. L. Zanchetta

Created on Jan 13, 2019
Revised on Aug 28, 2022

@author: rochford.peter1@gmail.com
@author: adlzanchetta@gmail.com
'''

import argparse
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import skill_metrics as sm

if __name__ == '__main__':

    # Define optional arguments for script
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-noshow', dest='no_show', action='store_true',
                            help="No figure is shown if this flag is present.")
    arg_parser.add_argument('-nosave', dest='no_save', action='store_true',
                            help="No figure is saved if this flag is present.")
    args = arg_parser.parse_args()
    del arg_parser

    # Set the figure properties (optional)
    rcParams["figure.figsize"] = [8.0, 6.4]
    rcParams['lines.linewidth'] = 1 # line width for plots
    rcParams.update({'font.size': 10}) # font size of axes text
    
    # Close any previously open graphics windows
    # ToDo: fails to work within Eclipse
    plt.close('all')
    
    # Store statistics in arrays
    sdev = np.array([129,113,83,29,107])
    crmsd = np.array([0,62,92,145,72])
    ccoef = np.array([1,.89,.73,.34,.83])
    bias  = np.array([1,.89,.73,.34,.83])

    # Specify labels for points in a cell array. Note that a label needs 
    # to be specified for the reference even
    label = ['Non-Dimensional Observation', 'ERA-interim', 'PERSSIAN-CCS', 
             'CMORPH', 'Rain Gage']
    
    '''
    Produce the Taylor diagram

    Label the points and change the axis options for SDEV, CRMSD, and CCOEF.
    Increase the upper limit for the SDEV axis and rotate the CRMSD contour 
    labels (counter-clockwise from x-axis). Exchange color and line style
    choices for SDEV, CRMSD, and CCOEFF variables to show effect. Increase
    the line width of all lines.

    For an exhaustive list of options to customize your diagram, 
    please call the function at a Python command line:
    >> taylor_diagram
    '''
    sm.taylor_diagram(sdev, crmsd, ccoef, markerLabel = label, 
                      locationColorBar = 'EastOutside',
                      markerDisplayed = 'colorBar', titleColorBar = 'Bias',
                      markerLabelColor='black', markerSize=10,
                      markerLegend='off', cmapzdata=bias,
                      colRMS='g', styleRMS=':', widthRMS=2.0, titleRMS='on',
                      colSTD='b', styleSTD='-.', widthSTD=1.0, titleSTD ='on',
                      colCOR='k', styleCOR='--', widthCOR=1.0, titleCOR='on')

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('taylor11.png', dpi=150, facecolor='w')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
