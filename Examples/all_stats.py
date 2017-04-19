from collections import OrderedDict

'''
How to obtain all the statistical metrics within the skill metrics 
library.

This is a simple program that provides examples of how to calculate the 
various skill metrics used or available in the library. All the 
calculated skill metrics are written to an Excel file for easy viewing
and manipulation. The Python code is kept to a minimum.

All functions in the Skill Metrics library are designed to only work 
with one-dimensional arrays, e.g. time series of observations at a 
selected location. The one-dimensional data are read in as dictionaries 
via a pickle file: ref['data'], pred1['data'], pred2['data'], and 
pred3['data']. The statistics are displayed to the screen as well as 
written to an Excel file named all_stats.xls.

The reference data used in this example are cell concentrations of a
phytoplankton collected from cruise surveys at selected locations and 
time. The model predictions are from three different simulations that
have been space-time interpolated to the location and time of the sample
collection. Details on the contents of the dictionary (once loaded) can 
be obtained by simply executing the following two statements

>> key_to_value_lengths = {k:len(v) for k, v in ref.items()}
>> print(key_to_value_lengths)
{'units': 6, 'longitude': 57, 'jday': 57, 'date': 57, 'depth': 57, 
'station': 57, 'time': 57, 'latitude': 57, 'data': 57}

Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com

Created on Nov 23, 2016

@author: prochford@thesymplectic.com
'''

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
    
    # Calculate various skill metrics, writing results to screen 
    # and Excel file. Use an ordered dictionary so skill metrics are 
    # saved in the Excel file in the same order as written to screen. 
    stats = OrderedDict()
            
    # Read data from pickle file
    data = load_obj('target_data')
    pred = data.pred1['data']
    ref = data.ref['data']

    # Get bias
    stats['bias'] = sm.bias(pred,ref)
    print('Bias = ' + str(stats['bias']))
    
    # Get Root-Mean-Square-Deviation (RMSD)
    stats['rmsd'] = sm.rmsd(pred,ref)
    print('RMSD = ' + str(stats['rmsd']))
    
    # Get Centered Root-Mean-Square-Deviation (CRMSD)
    stats['crmsd'] = sm.centered_rms_dev(pred,ref)
    print('CRMSD = ' + str(stats['crmsd']))
    
    # Get Standard Deviation (SDEV)
    stats['sdev'] = np.std(pred)
    print('SDEV = ' + str(stats['sdev']))
    
    # Get correlation coefficient (r)
    ccoef = np.corrcoef(pred,ref)
    stats['ccoef'] = ccoef[0,1]
    print('r = ' + str(stats['ccoef']))
    
    # Get Non-Dimensional Skill Score (SS)
    stats['ss'] = sm.skill_score_murphy(pred,ref)
    print('SS (Murphy) = ' + str(stats['ss']))
    
    # Get Brier Score (BS)
    forecast = np.array([0.7, 0.9, 0.8, 0.4, 0.2, 0, 0, 0, 0, 0.1])
    reference = np.array([0.9, 0.7, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0.1])
    observed = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 1])
    stats['bs'] = sm.brier_score(forecast,observed)
    print('SS (Brier) = ' + str(stats['bs']))
    
    # Get Non-Dimensional Forecast Skill Score (SS)
    stats['bss'] = sm.skill_score_brier(forecast,reference,observed)
    print('BSS = ' + str(stats['bss']))
    
    # Write statistics to Excel file.
    filename = 'all_stats.xlsx'
    sm.write_stats(filename,stats,overwrite=True)

    # Calculate statistics for target diagram
    target_stats1 = sm.target_statistics(data.pred1,data.ref,'data')

    # Write statistics to Excel file for a single data set
    filename = 'target_stats.xlsx'
    sm.write_target_stats(filename,target_stats1,overwrite = 'on')
      
    # Calculate statistics for Taylor diagram
    # The first array element corresponds to the reference series 
    # for the while the second is that for the predicted series.
    taylor_stats1 = sm.taylor_statistics(data.pred1,data.ref,'data')
    taylor_stats2 = sm.taylor_statistics(data.pred2,data.ref,'data')
    taylor_stats3 = sm.taylor_statistics(data.pred3,data.ref,'data')
 
    # Write statistics to Excel file
    filename = 'taylor_stats.xlsx'
    data = [taylor_stats1, taylor_stats2, taylor_stats3]
    title = ['Expt. 1', 'Expt. 2', 'Expt. 3']
    label = ['Observed', 'M1', 'M2', 'M3']
    sm.write_taylor_stats(filename,data,title = title, label = label, 
                       overwrite = True)

    # Check statistics for Taylor diagram
    diff = sm.check_taylor_stats(taylor_stats1['sdev'], 
                                 taylor_stats1['crmsd'], 
                                 taylor_stats1['ccoef'])
    print('Difference in Taylor statistics = ' + str(diff))
