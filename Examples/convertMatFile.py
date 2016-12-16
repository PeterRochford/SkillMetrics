'''
Program to convert a Matlab mat file in HDF5 format to a pickle file

This program was written to convert a Matlab "mat" file containing data 
structures to a pickle file containing dictionaries that could easily be 
read into Python. The version of scipy.io that was available would not read 
the mat files, so I was forced to use the h5py library to read the mat file
stored in Hierarchical Data Format version 5 (HDF5), store the data structures
in corresponding dictionaries and save them in individual pickle files.

The data structures in the mat file have the format: ref.data, pred1.data, 
pred2.data, and pred3.data. Each of these is stored in a separate pickle files:
ref.pkl, pred1.pkl, pred2.pkl, and pred3.pkl.

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

Created on Nov 23, 2016

@author: rochfordp
'''

# from Container import Container
import datetime as dt
import numpy as np, h5py
import pickle

def char2str(charArr):
    string = ''
    for x in charArr:
        string += chr(x)
    return string

def save_obj(obj, name):
    # Save object to file in pickle format
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    # Load object from file in pickle format
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def getDateTimeFromHDF5(fileHDF5,name):
    # Get list of dates in Python format
    nDate = len(f[name + '/value/date/value'].values())

    date = []
    time = []
    for i in range(nDate-1):
        dateVal = f[name + '/value/date/value/_%02d/value' % i]
        datestr = char2str(dateVal)
        dateObj = dt.date(int(datestr[0:4]),int(datestr[4:6]),int(datestr[6:8]))
        date.append(dateObj)

        timeVal = f[name + '/value/time/value/_%02d/value' % i]
        timestr = char2str(timeVal)
        timeObj = dt.time(int(timestr[0:2]),int(timestr[2:4]))
        time.append(timeObj)

    return date, time
    
class Container(object): 
    
    def __init__(self, pred1, pred2, pred3, ref):
        self.pred1 = pred1
        self.pred2 = pred2
        self.pred3 = pred3
        self.ref = ref
        
if __name__ == '__main__':
    matFile = 'target_data.mat'

    print 'Reading in data structures'
    f = h5py.File(matFile,'r')
    with f as hf:
#        print('List of items in the base directory:', hf.items())
        for name in f:
            print name 

            data = f[name + '/value/data/value']
            data = np.array(data.value[0])
            latitude = f[name + '/value/latitude/value']
            latitude = np.array(latitude.value[0])
            longitude = f[name + '/value/longitude/value']
            longitude = np.array(longitude.value[0])
            depth = f[name + '/value/depth/value']
            depth = np.array(depth.value[0])
            jday = f[name + '/value/jday/value']
            jday = np.array(jday.value[0])
            unitsValue = f[name + '/value/units/value']
            units = char2str(unitsValue.value)

            # Handle special cases for ref data structure
            if name == "ref":
                date, time = getDateTimeFromHDF5(f,name)               
                station = f[name + '/value/station/value']
                station = np.array(station.value[0])
            
            # Create dictionary and save to pickle file
            if name == "pred1":
                pred1 = {"data": data, "latitude": latitude, "longitude": longitude,
                         "depth": depth, "jday": jday, "units": units}
#                 save_obj(pred1,name)
            elif name == "pred2":
                pred2 = {"data": data, "latitude": latitude, "longitude": longitude,
                         "depth": depth, "jday": jday, "units": units}
#                 save_obj(pred2,name)
            elif name == "pred3":
                pred3 = {"data": data, "latitude": latitude, "longitude": longitude,
                         "depth": depth, "jday": jday, "units": units}
#                 save_obj(pred3,name)
            else:
                ref = {"data": data, "date": date, "depth": depth, 
                       "latitude": latitude, "longitude": longitude, 
                       "station": station, "time": time, "units": units, 
                       "jday": jday}
#                 save_obj(ref,name)

    # Create container for dictionaries
    data = Container(pred1, pred2, pred3, ref)
    
    # Save dictionaries to pickle file
    save_obj(data,'taylor_data')
    
    # Print summary
    print '\nSummary for ref:'
    key_to_value_lengths = {k:len(v) for k, v in ref.items()}
    print key_to_value_lengths
    
    print '\nFinished'
    