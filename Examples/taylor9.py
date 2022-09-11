'''
How to create a Taylor diagram with modified axes and data point colors
that show co-located points.

A ninth example of how to create a Taylor diagram given one set of
reference observations and multiple model predictions for the quantity.

This example is a variation on the fifth example (taylor5) where now a
legend is added, axes titles are suppressed, and four points are co-located 
(i.e. overly each other). Symbols with transparent faces are used so the 
co-located points can be seen. The list of points are checked for those 
that agree within 1% of each other and reported to the screen.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python taylor9.py -nosave

All functions in the Skill Metrics library are designed to only work with 
one-dimensional arrays, e.g. time series of observations at a selected location. 
The one-dimensional data are read in as dictionaries via Comma, Separated, 
Value (CSV) files:

data_files = ['pred1.csv', 'pred2.csv', 'pred3.csv', 'ref.csv']

This is done to make it easy for people who are new to Python to adapt this 
script to read their data. Refer to the load_data function for the format 
the CSV file must satisfy. 

The plot is written to a file in Portable Network Graphics (PNG) format, see
plt.savefig() below. Other formats are available by specifying the appropriate
file suffix for graphics supported by matplotlib. 

The reference data used in this example are cell concentrations of a
phytoplankton collected from cruise surveys at selected locations and 
time. The model predictions are from three different simulations that
have been space-time interpolated to the location and time of the sample
collection. Details on the contents of the dictionary (once loaded) can 
be obtained by simply executing the following two statements

>> key_to_value_lengths = {k:len(v) for k, v in data['ref'].items()}
>> print(key_to_value_lengths)
{'units': 6, 'longitude': 57, 'jday': 57, 'date': 57, 'depth': 57, 
'station': 57, 'time': 57, 'latitude': 57, 'data': 57}


Authors: Peter A. Rochford
         Andre D. L. Zanchetta

Created on Apr 22, 2017
Revised on Sep 11, 2022

@author: rochford.peter1@gmail.com
@author: adlzanchetta@gmail.com
'''

import argparse
from load_data import load_data
import matplotlib.pyplot as plt
import numpy as np
import skill_metrics as sm
from sys import version_info

if __name__ == '__main__':

    # Define optional arguments for script
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-noshow', dest='no_show', action='store_true',
                            help="No figure is shown if this flag is present.")
    arg_parser.add_argument('-nosave', dest='no_save', action='store_true',
                            help="No figure is saved if this flag is present.")
    args = arg_parser.parse_args()
    del arg_parser
    
    # Close any previously open graphics windows
    plt.close('all')
    
    # Read data from CSV files
    data_files = ['pred1.csv', 'pred2.csv', 'pred3.csv', 'ref.csv']
    data = load_data(data_files)

    # Calculate statistics for Taylor diagram
    # The first array element (e.g. taylor_stats1[0]) corresponds to the 
    # reference series while the second and subsequent elements
    # (e.g. taylor_stats1[1:]) are those for the predicted series.
    taylor_stats1 = sm.taylor_statistics(data['pred1'],data['ref'],'data')
    taylor_stats2 = sm.taylor_statistics(data['pred2'],data['ref'],'data')
    taylor_stats3 = sm.taylor_statistics(data['pred3'],data['ref'],'data')
    
    # Store statistics in arrays, making the fourth element a repeat of
    # the first.
    sdev = np.array([taylor_stats1['sdev'][0], taylor_stats1['sdev'][1], 
                     taylor_stats2['sdev'][1], taylor_stats3['sdev'][1],
                     taylor_stats1['sdev'][1], 0.991*taylor_stats3['sdev'][1]])
    crmsd = np.array([taylor_stats1['crmsd'][0], taylor_stats1['crmsd'][1], 
                      taylor_stats2['crmsd'][1], taylor_stats3['crmsd'][1],
                      taylor_stats1['crmsd'][1], taylor_stats3['crmsd'][1]])
    ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats1['ccoef'][1], 
                      taylor_stats2['ccoef'][1], taylor_stats3['ccoef'][1],
                      taylor_stats1['ccoef'][1], taylor_stats3['ccoef'][1]])

    # Specify labels for points in a cell array (M1 for model prediction 1,
    # etc.). Note that a label needs to be specified for the reference even
    # though it is not used.
    label = ['Non-Dimensional Observation', 'M1', 'M2', 'M3', 'M4', 'M5']
    
    # Check for duplicate statistics
    duplicateStats = sm.check_duplicate_stats(sdev[1:],crmsd[1:])
     
    # Report duplicate statistics, if any
    sm.report_duplicate_stats(duplicateStats)
    
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
    sm.taylor_diagram(sdev,crmsd,ccoef, markerLabel = label,
                      markerLabelColor = 'r', markerLegend = 'on', 
                      tickRMS = range(0,60,10), 
                      colRMS = 'm', styleRMS = ':', widthRMS = 2.0, 
                      titleRMS = 'on', titleRMSDangle = 40.0, tickSTD = range(0,80,20),
                      axismax = 60.0, colSTD = 'b', styleSTD = '-.', 
                      widthSTD = 1.0, titleSTD = 'on', 
                      colCOR = 'k', styleCOR = '--', widthCOR = 1.0, 
                      titleCOR = 'on', markerSize = 10, alpha = 0.0)

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('taylor9.png')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
