import pandas as pd

def is_list_of_strings(lst):
    '''
    Check if list contains only strings.

    Input:
    lst : list that may be all strings

    Returns:
      true if all strings
      false if not all strings

    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com
    
    Created on Apr 22, 2022
    '''
    
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False

def get_time_series(variables, CSVdata, **kwargs) -> dict:
    '''
    Extract time series data from a Pandas data frame obtained from a Comma Separated 
    Value (CSV) file.

    Input:
    variables : a string array of time series variables to be extracted as specified in the 
                column headers of the CSV file.
                If an empty list, then all time series variables are extracted
    data      : time series in a two-dimensional data structure with labeled axes
    *kwargs : variable-length keyword argument list. ??The keywords by 
              definition are dictionaries with keys that must correspond to 
              one choices given in OUTPUTS below.
    
    The format of data is a DataFrame as provided by the pandas.read_csv function. 

    Output:
    timeSeriesData : extracted time series in a dictionary with each variable in its own separate
                dictionary

    Each time series dictionary is of the form:

    CSV_variable = {"values": timeSeries, "units": units}
    
    where
    
    values : is a list containing the date time series
    units  : is the units for the variable
    
    For example, 
        {'values': [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, ... ], 'units': 'sec'}
    
    Author: Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Sep 11, 2022
    Revised on Sep 11, 2022
    '''

    nargin = len(kwargs)

    # Set default parameters for all options
    option = {}
    option['subsample'] = 0

    # Check data types of input variables
    
    # Test the data types of first two arguments
    if not isinstance(variables, list):
        raise ValueError('First argument is not a list')
    elif not isinstance(CSVdata, pd.DataFrame):
        raise ValueError('Second argument is not a Pandas DataFrame')
    
    # Check variables is list of strings
    if variables and not is_list_of_strings(variables):
        raise ValueError('First argument is not a string list')
    
    # Check for valid keys and values in dictionary
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if not optname in option:
            raise ValueError('Unrecognized option: ' + optname)
        else:
            # Replace option value with that from arguments
            option[optname] = optvalue

    # Find out contents of data
    labels = []
    for col in CSVdata.columns:
        labels.append(col.strip())

    timeSeriesData = {}
    if variables:
        # Extract requested data and return in a dictionary
        for name in variables:
            if name in labels:
                index = labels.index(name)
                timeSeries = CSVdata.iloc[:,index].tolist()
                if option['subsample'] > 0:
                    step = option['subsample']
                    timeSeries = timeSeries[0:-1:step]
                
                # Extract units if present and name dictionary to just variable
                start = name.find('(')
                end = name.find(')')
                if start != -1 and end != -1:
                    CSV_variable = name[0:start].strip()
                    units = name[start+1:end]
                else:
                    CSV_variable = name.strip()
                    units = ""
                
                # Create dictionary with value and units
                timeSeriesData[CSV_variable] = {"values": timeSeries, "units": units}
            else:
                raise ValueError('Variable ' + name + ' not in data.')
    else:
        # Extract all data and return in a dictionary
        index = 0
        while index < len(labels):
            name = labels[index]
            if name == 'hour':
                # Add hour and t(sec) to just t(sec)
                hour = CSVdata.iloc[:,index].tolist()
                index += 1
                time = CSVdata.iloc[:,index].tolist()
                timeSeries = []
                for x in range(0,len(hour)):
                    timeSeries.append(3600*hour[x] + time[x])
            else:
                timeSeries = CSVdata.iloc[:,index].tolist()
            
            # Extract units if present and name dictionary to just variable
            start = name.find('(')
            end = name.find(')')
            if start != -1 and end != -1:
                CSV_variable = name[0:start].strip()
                units = name[start+1:end]
            else:
                CSV_variable = name.strip()
                units = ""
            
            # Create dictionary with value and units
            timeSeriesData[CSV_variable] = {"values": timeSeries, "units": units}
            index += 1

    return timeSeriesData
