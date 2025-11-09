'''
How to create a Taylor diagram with no centered RMSD contours

A thirteenth example of how to create a Taylor diagram given one set of
reference observations and two sets of model predictions for the quantity. 
This is a variant of example 12, but where the centered RMSD contours 
are suppressed.

This example shows how to display multiple data sets on the same Taylor 
diagram where a different color marker is used for each data set to
identify its source. This is accomplished by overlaying the points from
the second data set onto the Taylor diagram created using the first data 
set. Three data sets are used in this example where one is the reference
and the other two are model predictions. This example also shows how to
specify the legend using a dictionary instead of a list.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python taylor13.py -nosave

The data sets are yearly time series for years 2001-2014, each stored as
a list in a dictionary having a key of the form 'spi_2001', 'spi_2002', etc.
There is a separate dictionary for each of the observation data set and the 
two model predictions. Each dictionary is written to its own pickle file. 
A different file suffix is used depending upon whether the file is created 
using Python 2 (.pkl) or Python 3 (.pkl3) because the pickle package is not 
cross version compatible for pickle files containing dictionaries.

The data in these files are statistics calculated from yearly time series of 
Standard Precipitation Index value over the Mekong basin, a trans-boundary 
river in Southeast Asia that originates in the Tibetan Plateau and runs 
through China's Yunnan Province, Myanmar, Laos, Thailand, Cambodia, and Vietnam. 
The data sources are the ERA5 climate reanalysis dataset from the European 
Centre for Medium-Range Weather Forecasts (ECMWF) and the Tropical Rainfall 
Measuring Mission (TRMM 3B42 v7) satellite data, whilst the observation data is 
the Asian Precipitation - Highly-Resolved Observational Data Integration 
Towards Evaluation (APHRODITE V1801R1) rain-gauge data. All the statistics for 
the yearly time series are calculated as a function of the year, i.e. 2001 ERA5
and TRMM are calculated using APHRODITE 2001, 2002 ERA5 and TRMM are calculated 
using APHRODITE 2002, etc.

Note that the centered RMSD contours are suppressed for this Taylor diagram. 
This is important because the origin for the RMSD contours is specified by the 
standard deviation of the observations as dictated by the Taylor relationship. 
While statistics for each data point can be calculated using observations for 
that year and displayed on the diagram, there is no universal set of RMSD contours 
to correctly indicate the centered RMSD values of the different points, because 
each point is associated with a different observation standard deviation, and 
hence each has a different set of RMS contours with its own distinct origin. To
show statistics respect to reference time series of the same year, one must 
suppress the RMSD contours, as otherwise it would provide a misleading indication 
of the centered RMSD values.

This data was provided courtesy of Iacopo Ferrario, Resources Scientist, 
HR Wallingford, Flood and Water Resources group, Wallingford Oxfordshire,
United Kingdom

Authors: Peter A. Rochford
         Andre D. L. Zanchetta

Created on Feb 26, 2019
Revised on Aug 28, 2022

@author: rochford.peter1@gmail.com
@author: adlzanchetta@gmail.com
'''

import argparse
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pickle
import skill_metrics as sm
from sys import version_info

def load_obj(name):
    # Load object from file in pickle format
    if version_info[0] == 2:
        suffix = 'pkl'
    else:
        suffix = 'pkl3'

    with open(name + '.' + suffix, 'rb') as f:
        return pickle.load(f) # Python2 succeeds
    
class Container(object): 
    def __init__(self, target_stats1, target_stats2, taylor_stats1, taylor_stats2):
        self.target_stats1 = target_stats1
        self.target_stats2 = target_stats2
        self.taylor_stats1 = taylor_stats1
        self.taylor_stats2 = taylor_stats2

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
    rcParams["figure.figsize"] = [6.0, 4.8]
    rcParams['lines.linewidth'] = 1 # line width for plots
    rcParams.update({'font.size': 12}) # font size of axes text
    
    # Close any previously open graphics windows
    # ToDo: fails to work within Eclipse
    plt.close('all')
    
    # Read Taylor statistics for ERA Interim (stats1) and TRMM (stats2) 
    # data with respect to APHRODITE observations for each of years 2001 to 
    # 2014 from pickle file
    stats = load_obj('Mekong_Basin_data_interannual') # observations

    # Specify labels for points in a dictionary because only desire labels
    # for each data set.
    label = {'ERA-5': 'r', 'TRMM': 'b'}
    
    '''
    Produce the Taylor diagram for the first dataset
    '''
    sm.taylor_diagram(stats.taylor_stats1['sdev'], 
                      stats.taylor_stats1['crmsd'], 
                      stats.taylor_stats1['ccoef'], markercolor = str(label['ERA-5']), alpha = 0.0,
                      titleRMS = 'off', showlabelsRMS = 'off', tickRMS =[0.0])

    '''
    Overlay the second dataset
    '''
    sm.taylor_diagram(stats.taylor_stats2['sdev'], 
                      stats.taylor_stats2['crmsd'], 
                      stats.taylor_stats2['ccoef'], markercolor = str(label['TRMM']), alpha = 0.0,
                      overlay = 'on', markerLabel = label)

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('taylor13.png', dpi=150, facecolor='w')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
