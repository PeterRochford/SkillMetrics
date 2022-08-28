'''
How to create a Taylor diagram with a large number of symbols of
different color along with a legend.

A tenth example of how to create a Taylor diagram given one set of
reference observations and multiple model predictions for the quantity.

Produces a Taylor diagram showing how data available from public sources 
can be used to populate an acceptable model of water temperatures in the 
Farmington River basin of Connecticut.

The data are stored in arrays named: sdev, crmsd, ccoef, and gageID. Each of 
these contain 1 reference value (first position) and 22 prediction values, 
for a total of 23 values. These arrays are stored in a container which is 
then written to a pickle file. A different file suffix is used depending upon 
whether the file is created using Python 2 (.pkl) or Python 3 (.pkl3) because 
the pickle package is not cross version compatible for pickle files containing 
containers of dictionaries.

The source data is an observation set at each location as well as a 
simulation set. The reference value is chosen that more or less represents 
the consensus on acceptable values of the root-mean square error.

This data was provide courtesy of John Yearsley, Affiliate Professor,
UW-Hydro|Computational Hydrology, University of Washington (Yearsley et al., 
2019).

References:

Yearsley, J. R., Sun, N., Baptiste, M., and Nijssen, B. (2019) Assessing the 
  Impacts of Hydrologic and Land Use Alterations on Water Temperature in the 
  Farmington River Basin in Connecticut, Hydrol. Earth Syst. Sci. Discuss., 
  https://doi.org/10.5194/hess-2019-94, 
  https://www.hydrol-earth-syst-sci-discuss.net/hess-2019-94/hess-2019-94.pdf

Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com

Created on Dec 5, 2019

@author: prochford@thesymplectic.com
'''

import matplotlib.pyplot as plt
import numpy as np
import pickle
import skill_metrics as sm
from sys import version_info
import argparse


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

    # Defines the output file name or path 
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-noshow', dest='no_show', action='store_true',
                            help="No figure is shown if this flag is present.")
    arg_parser.add_argument('-nosave', dest='no_save', action='store_true',
                            help="No figure is saved if this flag is present.")
    args = arg_parser.parse_args()
    del arg_parser
    
    # Close any previously open graphics windows
    # ToDo: fails to work within Eclipse
    plt.close('all')
        
    # Read data from pickle file
    data = load_obj('Farmington_River_data')
    
    # Change number of data points to illustrate effect
    # of changing number of columns
    ncol = 2
    if ncol == 1:
        sdev = data.sdev[0:11]
        crmsd = data.crmsd[0:11]
        ccoef = data.ccoef[0:11]
        gageID = data.gageID[0:11]
    elif ncol == 2:
        sdev = data.sdev
        crmsd = data.crmsd
        ccoef = data.ccoef
        gageID = data.gageID
    else:
        sdev = data.sdev
        crmsd = data.crmsd
        ccoef = data.ccoef
        gageID = data.gageID
        sdev = np.append(sdev,data.sdev[1:11])
        crmsd = np.append(crmsd,data.crmsd[1:11])
        ccoef = np.append(ccoef,data.ccoef[1:11])
        gageID = gageID + data.gageID[1:11]
    
    # Specify labels for points in a cell array using gage ID.
    label = gageID
    
    # Must set figure size here to prevent legend from being cut off
    plt.figure(num=1, figsize=(8, 6))

    
    '''
    Produce the Taylor diagram

    Label the points and change the axis options for SDEV, CRMSD, and CCOEF.
    Increase the upper limit for the SDEV axis and rotate the CRMSD contour 
    labels (counter-clockwise from x-axis). Exchange color and line style
    choices for SDEV, CRMSD, and CCOEFF variables to show effect. Increase
    the line width of all lines. Suppress axes titles and add a legend.

    For an exhaustive list of options to customize your diagram, 
    please call the function at a Python command line:
    >> taylor_diagram
    '''    
    sm.taylor_diagram(sdev,crmsd,ccoef, markerLabel = label, markerLabelColor = 'r', 
                      markerLegend = 'on', markerColor = 'r',
                      styleOBS = '-', colOBS = 'r', markerobs = 'o',
                      markerSize = 6, tickRMS = [0.0, 1.0, 2.0, 3.0],
                      tickRMSangle = 115, showlabelsRMS = 'on',
                      titleRMS = 'on', titleOBS = 'Ref')

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('taylor10.png')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
