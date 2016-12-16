'''
How to create a taylor diagram with overlaid markers

A seventh example of how to create a Taylor diagram given one set
of reference observations and multiple model predictions for the
quantity.

This example is a variation on the sixth example (taylor6) where now a
fourth data point having a negative correlation is overlaid on an
existing Taylor diagram that already has 3 data points with positive
correlations. It is chosen to have data points with positive correlations
appear in red while data points with negative correlations are displayed
in blue.  

All functions in the Skill Metrics library are designed to only work with
one-dimensional arrays, e.g. time series of observations at a selected
location. The one-dimensional data are read in as dictionaries via a 
pickle file: ref['data'], pred1['data'], pred2['data'], 
and pred3['data']. The plot is written to a file in Portable Network 
Graphics (PNG) format.

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
        Acorn Science & Innovation
        prochford@acornsi.com

Created on Dec 7, 2016

@author: rochfordp
'''

import matplotlib.pyplot as plt
import numpy as np
import pickle
import skill_metrics as sm

def load_obj(name):
    # Load object from file in pickle format
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Container(object): 
    
    def __init__(self, pred1, pred2, pred3, ref):
        self.pred1 = pred1
        self.pred2 = pred2
        self.pred3 = pred3
        self.ref = ref
        
if __name__ == '__main__':
    
    # Close any previously open graphics windows
    # ToDo: fails to work within Eclipse
    plt.close('all')
        
    # Read data from pickle file
    data = load_obj('taylor_data')

    # Calculate statistics for Taylor diagram
    # The first array element corresponds to the reference series 
    # for the while the second is that for the predicted series.
    taylor_stats1 = sm.taylor_statistics(data.pred1,data.ref,'data')
    taylor_stats2 = sm.taylor_statistics(data.pred2,data.ref,'data')
    taylor_stats3 = sm.taylor_statistics(data.pred3,data.ref,'data')
    
    # Store statistics in arrays
    sdev = np.array([taylor_stats1['sdev'][0], taylor_stats1['sdev'][1], 
                     taylor_stats2['sdev'][1], taylor_stats3['sdev'][1]])
    crmsd = np.array([taylor_stats1['crmsd'][0], taylor_stats1['crmsd'][1], 
                      taylor_stats2['crmsd'][1], taylor_stats3['crmsd'][1]])
    ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats1['ccoef'][1], 
                      taylor_stats2['ccoef'][1], taylor_stats3['ccoef'][1]])

    # Specify labels for points in a cell array (M1 for model prediction 1,
    # etc.). Note that a label needs to be specified for the reference even
    # though it is not used.
    label = ['Non-Dimensional Observation', 'M1', 'M2', 'M3']
    
    '''
    Produce the Taylor diagram

    Display the data points for correlations that vary from -1 to 1 (2
    panels). Label the points and change the axis options for SDEV, CRMSD,
    and CCOEF. Increase the upper limit for the SDEV axis and rotate the
    CRMSD contour labels (counter-clockwise from x-axis). Exchange color and
    line style choices for SDEV, CRMSD, and CCOEFF variables to show effect.
    Increase the line width of all lines.

    For an exhaustive list of options to customize your diagram, 
    please call the function at a Python command line:
    >> taylor_diagram
    '''
    sm.taylor_diagram(sdev,crmsd,ccoef,
                      numberPanels = 2,
                      markerLabel = label, markerLabelColor = 'r',
                      tickRMS = range(0,90,10), tickRMSangle = 150.0,
                      colRMS = 'g', styleRMS = ':', widthRMS = 2.0, 
                      titleRMS = 'off',
                      tickSTD = range(0, 80, 20), axismax = 60.0,
                      colSTD = 'b', styleSTD = '-.', widthSTD = 1.0,
                      colCOR = 'k', styleCOR = '--', widthCOR = 1.0)

    # Calculate a negative correlation for one of the data values.
    data.pred3['data'] = -data.pred3['data']
    taylor_stats3 = sm.taylor_statistics(data.pred3,data.ref,'data')
    sdev = np.array([taylor_stats3['sdev'][0], taylor_stats3['sdev'][1]])
    crmsd = np.array([taylor_stats3['crmsd'][0], taylor_stats3['crmsd'][1]])
    ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats3['ccoef'][1]])
    
    # Overlay new data point (blue) on existing diagram
    label = ['Non-Dimensional Observation', 'M4']
    sm.taylor_diagram(sdev,crmsd,ccoef, overlay = 'on',
                      markerLabel = label, markerLabelColor = 'b',
                      markerColor = 'b')

    # Write plot to file
    plt.savefig('taylor7.png')

    # Show plot
    plt.show()
