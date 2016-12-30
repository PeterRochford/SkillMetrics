import os
import xlsxwriter

def write_stats(filename,data,**kwargs):
    '''
    Write statistics to an Excel file.
    
    This function writes to an Excel file FILENAME the statistics 
    provided in each of the dictionaries contained in DATA. The first 
    2 arguments must be the inputs as described below followed by 
    keyword arguments in the format of OPTION = VALUE. Each statistic 
    will be labeled according to the name under which it is stored in 
    the DATA data structure, e.g. data.bias will be labeled as "bias".
   
    INPUTS:
    filename     : name for statistics Excel file
    data         : a dictionary containing the statistics
    data['stat'] : statistics, e.g. data.bias for Bias.
   
    OUTPUTS:
        None.
   
    LIST OF OPTIONS:
      A title description for each dictionary (TITLE) can be 
    optionally provided as well as an overwrite option if the file 
    name currently exists.
   
    title = title : title descriptor data set, e.g. 'Expt. 01.0'
    overwrite = boolean : true/false flag to overwrite Excel file
  
    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Dec 10, 2016
    '''

    option = get_write_stats_options(**kwargs)
    
    # Check for existence of file
    if os.path.isfile(filename):
        if option['overwrite']:
            os.remove(filename)
        else:
            ValueError('File already exists: ' + filename)
    
    # Write title information to file
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
     
    # Write descriptive title
    if len(option['title']) > 0:
        worksheet.write(1, 0, option['title'])
    else:
        worksheet.write(1, 0, 'Skill Metrics')
    
    # Determine number of elements in the dictionary lists and write 
    # appropriate header
    worksheet.write(3, 0, 'Skill Metric')
    ncell = len(data.items()[0]) - 1
    for i in range(ncell):
        worksheet.write(3, i+1, 'Case ' + str(i+1))

    # Write data of all the fields
    row = 4
    col = 0
    for key, value in data.items():
        worksheet.write(row, col, key)
        for i,v in enumerate([value]):
            worksheet.write(row, col + 1 + i, v)
        row += 1

    workbook.close()

def get_write_stats_options(**kwargs):
    '''
    Get optional arguments for write_stats function.

    Retrieves the keywords supplied to the WRITE_STATS function (**KWARGS), 
    and returns the values in a OPTION dicitonary. Default values are 
    assigned to selected optional arguments. The function will terminate
    with an error if an unrecognized optional argument is supplied.
 
    INPUTS:
    **kwargs : keyword argument list
 
    OUTPUTS:
    option : data structure containing option values.
    option['title']     : title descriptor for data set.
    option['overwrite'] : boolean to overwrite Excel file.
   
    LIST OF OPTIONS:
      A title description for each dataset TITLE can be optionally 
    provided as well as an overwrite option if the file name currently
    exists.
   
    title = title : title descriptor for each data set in data, e.g. 
                   'Expt. 01.0'
    overwrite = boolean : true/false flag to overwrite Excel file
  
    Author: Peter A. Rochford
    Acorn Science & Innovation
    prochford@acornsi.com

    Created on Dec 10, 2016

    @author: rochfordp  
    '''
    from skill_metrics import check_on_off

    nargin = len(kwargs)

    #  Set default parameters
    option = {}
    option['title'] = ''
    option['overwrite'] = False
    if nargin == 0:
        # No options requested, so return with only defaults
        return option

    # Load custom options, storing values in option data structure
        
    # Check for valid keys and values in dictionary
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if not optname in option:
            raise ValueError('Unrecognized option: ' + optname)
        else:
            # Replace option value with that from arguments
            option[optname] = optvalue
            
            # Check values for specific options
            if optname == 'overwrite':
                option['overwrite'] = check_on_off(option['overwrite'])

    return option
