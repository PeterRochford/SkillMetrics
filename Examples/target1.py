'''
How to create a simple target diagram

A first example of how to create a simple target diagram given one set of
reference observations and multiple model predictions for the quantity.
The Python code is kept to a minimum.

This example shows how to calculate the required statistics and produce
the target diagram. All functions in the Skill Metrics library are
designed to only work with one-dimensional arrays, e.g. time series of
observations at a selected location. The one-dimensional data are read in
as dictionaries via a pickle file: ref['data'], pred1['data'], pred2['data'], 
and pred3['data']. The plot is written to a file in Portable Network Graphics
(PNG) format.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python target1.py -noshow

The reference data used in this example are cell concentrations of a
phytoplankton collected from cruise surveys at selected locations and 
time. The model predictions are from three different simulations that
have been space-time interpolated to the location and time of the sample
collection. Details on the contents of the dictionary (once loaded) can 
be obtained by simply executing the following two statements

>> key_to_value_lengths = {k:len(v) for k, v in ref.items()}
>> print key_to_value_lengths
{'units': 6, 'longitude': 57, 'jday': 57, 'date': 57, 'depth': 57, 
'station': 57, 'time': 57, 'latitude': 57, 'data': 57}

Author: Peter A. Rochford

Created on Nov 23, 2016
Revised on Aug 28, 2022

@author: rochford.peter1@gmail.com
'''

import argparse
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
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
    
    def __init__(self, pred1, pred2, pred3, ref):
        self.pred1 = pred1
        self.pred2 = pred2
        self.pred3 = pred3
        self.ref = ref
        
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
    rcParams["figure.figsize"] = [8.0, 6.4] #works
#     rcParams['lines.linewidth'] = 2 # line width for plots
    rcParams.update({'font.size': 12}) # font size of axes text

    # Close any previously open graphics windows
    plt.close("all")
        
    # Read data from pickle file
    data = load_obj('target_data')

    # Calculate statistics for target diagram
    target_stats1 = sm.target_statistics(data.pred1,data.ref,'data')
    target_stats2 = sm.target_statistics(data.pred2,data.ref,'data')
    target_stats3 = sm.target_statistics(data.pred3,data.ref,'data')
     
    # Store statistics in arrays
    bias = np.array([target_stats1['bias'], target_stats2['bias'], 
                     target_stats3['bias']])
    crmsd = np.array([target_stats1['crmsd'], target_stats2['crmsd'], 
                      target_stats3['crmsd']])
    rmsd = np.array([target_stats1['rmsd'], target_stats2['rmsd'], 
                     target_stats3['rmsd']])

    '''
    Produce the target diagram
    
    Reference circles are plotted at the maximum range of the axes and at 0.7
    times the maximum range by default.
    '''
    sm.target_diagram(bias,crmsd,rmsd)

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('target1.png')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
    
