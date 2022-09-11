import os
from read_csv_data import read_csv_data

def load_data(filenames : list) -> dict:
    '''
    Reads data from Comma, Separated, Value (CSV) files and returns them in dictionary objects.
    
    This function accepts a list of CSV filenames and returns a dictionary containing the 
    contents of all the files. Each key in the dictionary is the prefix of the filename, 
    e.g. pred1 for a file named pred1.csv, so for a returned dictionary named "data" this 
    would be data['pred1']. 
    
    The contents of the file are stored as lists in the dictionary, so for a column named 'data'
    in the CSV file example above, the data would be accessed using data['pred1']['data']. 
     
    INPUTS:
    filenames : list of CSV filenames, e.g.
                filenames = ['pred1.csv', 'pred2.csv', 'pred3.csv', 'ref.csv']
    
    OUTPUTS:
    data : dictionary containing keys of dictionaries of the data in the CSV files

    The CSV file format must conform to that described in the read_element_data function. An 
    example of the format for the contents of a CSV file is 
    
     data        latitude    longitude    depth    jday            units
0    52.9110002  43.161833   -69.576667   -1       3045.255556     cell/L
1    1.431675565 43.161833   -69.576667   -10      3045.255556     cell/L
2    1.280270828 43.161833   -69.576667   -20      3045.255556     cell/L
...
55   0.391304068 42.964333   -69.7645     -20      3045.979861     cell/L
56   0.360104567 42.964333   -69.7645     -30      3045.979861     cell/L

[56 rows x 7 columns]

    Created on Sep 10, 2022
    Revised on Sep 10, 2022
    
    Author: Peter A. Rochford
        rochford.peter1@gmail.com
    '''
    
    # Create empty dictionary
    data = {}
    
    # Process list of filenames
    for name in filenames:
        # Read data from provided CSV file
        csv_data = read_csv_data(name)
        
        # Convert pandas data frame to dictionary
        dict_data = csv_data.to_dict('list')

        # Get prefix of file name
        file_name, file_extension = os.path.splitext(name)
        
        # Store data as key in dictionary
        data[file_name] = dict_data
        
        del csv_data, dict_data
    
    return data
