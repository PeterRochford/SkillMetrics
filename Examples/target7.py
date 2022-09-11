'''
How to create a target diagram with a legend plus changed marker colors 
and circles that show co-located points.

A seventh example of how to create a target diagram given one set of
reference observations and multiple model predictions for the quantity.

This example is a variation on the fourth example (target4) where now a
legend is added, the marker colors are changed, the radii of circles
to draw are specified, and two points are co-located 
(i.e. overly each other). Symbols with transparent faces are used so the 
co-located points can be seen. The list of points are checked for those 
that agree within 1% of each other and reported to the screen.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python target7.py -noshow

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


Author: Peter A. Rochford

Created on Dec 1, 2016
Revised on Aug 28, 2022

@author: rochford.peter1@gmail.com
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

    # Calculate statistics for target diagram
    target_stats1 = sm.target_statistics(data['pred1'],data['ref'],'data')
    target_stats2 = sm.target_statistics(data['pred2'],data['ref'],'data')
    target_stats3 = sm.target_statistics(data['pred3'],data['ref'],'data')
     
    # Store statistics in arrays, making the fourth element a repeat of
    # the first.
    bias = np.array([target_stats1['bias'], target_stats2['bias'], 
                     target_stats3['bias'], target_stats1['bias'],
                     0.991*target_stats3['bias']])
    crmsd = np.array([target_stats1['crmsd'], target_stats2['crmsd'], 
                      target_stats3['crmsd'], target_stats1['crmsd'],
                      target_stats3['crmsd']])
    rmsd = np.array([target_stats1['rmsd'], target_stats2['rmsd'], 
                     target_stats3['rmsd'], target_stats1['rmsd'],
                     target_stats3['rmsd']])

    # Specify labels for points in a list (M1 for model prediction # 1, 
    # etc.).
    label = ['M1', 'M2', 'M3', 'M4', 'M5']
    
    # Check for duplicate statistics
    duplicateStats = sm.check_duplicate_stats(bias,crmsd)
     
    # Report duplicate statistics, if any. 
    sm.report_duplicate_stats(duplicateStats)

    '''
    Produce the target diagram

    Label the points and change the axis options. Increase the upper limit
    for the axes, change color and line style of circles. Increase
    the line width of circles. Change color of labels and points. Add a
    legend.

    For an exhaustive list of options to customize your diagram, 
    please call the function at a Python command line:
    >> target_diagram
    '''
    
    sm.target_diagram(bias,crmsd,rmsd, markerLabel = label, \
                      markerLabelColor = 'b', markerLegend = 'on', \
                      ticks = np.arange(-50,60,10), \
                      axismax = 50.0, \
                      circles = [20, 40, 50], \
                      circleLineSpec = 'b-.', circleLineWidth = 1.5,
                      markerSize = 10, alpha = 0.0)

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('target7.png')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
    