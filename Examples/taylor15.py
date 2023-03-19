'''
How to create a Taylor diagram with a large number of symbols of
different color along with a legend.

A fifteenth example of how to create a Taylor diagram with individual 
control of the marker symbols, color, type, size, etc. This allows the
user to have custom control over the appearance of the markers and the
legend. However, it requires the user to specify all the details for each 
marker in a dictionary where the key is the marker label provided as a 
string. For example, for river gauge "14197":

MARKERS = {
    "14197": {              # marker label
        "labelColor": "k",  # label color of black
        "symbol": "+",      # plus marker symbol
        "size": 9,          # marker size of 9 pt
        "faceColor": "r",   # marker face color of red
        "edgeColor": "r",   # marker edge color of red
    }

It supports the following arguments as options.

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution:

$ python taylor15.py -nosave

The Taylor diagram created is for a model of water temperatures in the
Farmington River basin of Connecticut. This script is based on Taylor diagram 
example 10. 

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

Authors: Peter A. Rochford
         Andre D. L. Zanchetta

Created on Dec 5, 2019
Revised on Aug 28, 2022

@author: rochford.peter1@gmail.com
@author: adlzanchetta@gmail.com
'''

import argparse
import matplotlib.pyplot as plt
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
    
    def __init__(self, bias, sdev, crmsd, ccoef, rmsd, gageID):
        self.bias = bias
        self.sdev = sdev
        self.crmsd = crmsd
        self.ccoef = ccoef
        self.rmsd = rmsd
        self.gageID = gageID
        
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
    # ToDo: fails to work within Eclipse
    plt.close('all')
        
    # Read data from pickle file
    data = load_obj('Farmington_River_data')
    
    '''
    Specify individual marker label (key), label color, symbol, size, symbol face color, 
    symbol edge color
    '''
    MARKERS = {
        "14197": {
            "labelColor": "k",
            "symbol": "+",
            "size": 9,
            "faceColor": "r",
            "edgeColor": "r",
        },
        "14442": {
            "labelColor": "gray",
            "symbol": ".",
            "size": 9,
            "faceColor": "b",
            "edgeColor": "b",
        },
        "14713": {
            "labelColor": "k",
            "symbol": "x",
            "size": 9,
            "faceColor": "g",
            "edgeColor": "g",
        },
        "14484": {
            "labelColor": "gray",
            "symbol": "s",
            "size": 9,
            "faceColor": "c",
            "edgeColor": "c",
        },
        "14841": {
            "labelColor": "k",
            "symbol": "d",
            "size": 9,
            "faceColor": "m",
            "edgeColor": "m",
        },
        "15240": {
            "labelColor": "gray",
            "symbol": "^",
            "size": 9,
            "faceColor": "y",
            "edgeColor": "y",
        },
        "15320": {
            "labelColor": "k",
            "symbol": "v",
            "size": 9,
            "faceColor": "r",
            "edgeColor": "r",
        },
        "15516": {
            "labelColor": "gray",
            "symbol": "p",
            "size": 9,
            "faceColor": "b",
            "edgeColor": "b",
        },
        "15571": {
            "labelColor": "k",
            "symbol": "h",
            "size": 9,
            "faceColor": "g",
            "edgeColor": "g",
        },
        "15790": {
            "labelColor": "gray",
            "symbol": "*",
            "size": 9,
            "faceColor": "c",
            "edgeColor": "c",
        },
        "15792": {
            "labelColor": "k",
            "symbol": "+",
            "size": 9,
            "faceColor": "m",
            "edgeColor": "m",
        },
        "15825": {
            "labelColor": "gray",
            "symbol": ".",
            "size": 9,
            "faceColor": "y",
            "edgeColor": "y",
        },
        "15844": {
            "labelColor": "k",
            "symbol": "x",
            "size": 9,
            "faceColor": "r",
            "edgeColor": "r",
        },
        "16058": {
            "labelColor": "gray",
            "symbol": "s",
            "size": 9,
            "faceColor": "b",
            "edgeColor": "b",
        },
        "16059": {
            "labelColor": "k",
            "symbol": "d",
            "size": 9,
            "faceColor": "g",
            "edgeColor": "g",
        },
        "16060": {
            "labelColor": "gray",
            "symbol": "^",
            "size": 9,
            "faceColor": "c",
            "edgeColor": "c",
        },
        "16066": {
            "labelColor": "k",
            "symbol": "v",
            "size": 9,
            "faceColor": "m",
            "edgeColor": "m",
        },
        "16091": {
            "labelColor": "gray",
            "symbol": "p",
            "size": 9,
            "faceColor": "y",
            "edgeColor": "y",
        },
        "17338": {
            "labelColor": "k",
            "symbol": "h",
            "size": 9,
            "faceColor": "r",
            "edgeColor": "r",
        },
        "17364": {
            "labelColor": "gray",
            "symbol": "*",
            "size": 9,
            "faceColor": "b",
            "edgeColor": "b",
        },
        "17365": {
            "labelColor": "k",
            "symbol": "+",
            "size": 9,
            "faceColor": "g",
            "edgeColor": "g",
        },
        "17437": {
            "labelColor": "gray",
            "symbol": ".",
            "size": 9,
            "faceColor": "c",
            "edgeColor": "c",
        },
    }
    
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
    sm.taylor_diagram(sdev,crmsd,ccoef, markers = MARKERS, 
                      markerLegend = 'on', styleOBS = '-', colOBS = 'r', markerobs = 'o',
                      tickRMS = [0.0, 1.0, 2.0, 3.0],
                      tickRMSangle = 115, showlabelsRMS = 'on',
                      titleRMS = 'on', titleOBS = 'Ref')
    
    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('taylor15.png')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()
