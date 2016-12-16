import os
import xlsxwriter

def write_taylor_stats(filename,data,**kwargs):
    '''
    Write statistics used in a target diagram to an Excel file.
    
    This function writes to an Excel file FILENAME the statistics 
    used to create a Taylor diagram for each of the dictionaries 
    contained in DATA. The first 2 arguments must be the inputs as 
    described below followed by keyword arguments in the format of 
    OPTION = VALUE.
   
    INPUTS:
    filename      : name for statistics Excel file
    data          : a dictionary containing the statistics
    data['sdev']  : Standard deviations (sigma)
    data['crmsd'] : Centered Root Mean Square Difference (CRMSD)
    data['ccoef'] : Correlation Coefficient (r)
   
    OUTPUTS:
        None.
   
    LIST OF OPTIONS:
      A title description for each dictionary (TITLE) can be 
    optionally provided as well as a LABEL for each data point in 
    the diagram.
   
    label = label : label for each data point in target diagram, e.g. 
                    'OC445 (CB)'
    overwrite = boolean : true/false flag to overwrite Excel file
    title = title : title descriptor data set, e.g. 'Expt. 01.0'
  
    Author: Peter A. Rochford
    Acorn Science & Innovation
    prochford@acornsi.com

    Created on Dec 12, 2016

    @author: rochfordp  
    '''

    option = get_write_taylor_stats_options(**kwargs)
    
    # Check for existence of file
    if os.path.isfile(filename):
        if option['overwrite']:
            os.remove(filename)
        else:
            ValueError('File already exists: ' + filename)
    
    # Covert data to list if necessary
    if not type(data) is list: data = [data]

    # Write title information to file
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
     
    # Write title information to file
    worksheet.write(1, 0, 'Taylor Statistics')

    # Determine number of dictionaries in data variable
    ncell = len(data)
    
    # Write data for each dictionary
    row = 2
    headers = ['Description','Standard Deviation','CRMSD','Correlation Coeff.']
    for i in range(ncell):
        row += 1
        if len(option['title']) > 0:
            worksheet.write(row, 0, option['title'][i])

        # Write column headers
        row += 1
        for j,h in enumerate(headers):
            worksheet.write(row, j, h)

        # Retrieve input values as list
        try: iter(data[i]['sdev'])
        except TypeError:
            sdev = [data[i]['sdev']]
            crmsd = [data[i]['crmsd']]
            ccoef = [data[i]['ccoef']]
        else:
            sdev = data[i]['sdev']
            crmsd = data[i]['crmsd']
            ccoef = data[i]['ccoef']
        ndata = len(sdev)

        # Write each row of data
        row += 1
        for j in range(ndata):
            if len(option['label']) > 0:
                worksheet.write(row, 0, option['label'][j])
    
            worksheet.write(row, 1, sdev[j])
            worksheet.write(row, 2, crmsd[j])
            worksheet.write(row, 3, ccoef[j])
            row += 1

    workbook.close()

def get_write_taylor_stats_options(**kwargs):
    '''
    Get optional arguments for write_taylor_stats function.

    Retrieves the keywords supplied to the WRITE_TARGET_STATS 
    function (**KWARGS), and returns the values in a OPTION dictionary. 
    Default values are assigned to selected optional arguments. The 
    function will terminate with an error if an unrecognized optional 
    argument is supplied.
 
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
   
    label = label : label for each data point in target diagram, e.g. 
                    'OC445 (CB)'
    overwrite = boolean : true/false flag to overwrite Excel file
    title = title : title descriptor for each data set in data, e.g. 
                   'Expt. 01.0'
  
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
    option['overwrite'] = False
    option['label'] = []
    option['title'] = ''
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
