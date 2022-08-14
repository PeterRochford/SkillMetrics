from skill_metrics.use_sci_notation import use_sci_notation

def get_axis_tick_label(value):
    '''
    Get label for number on axis without trailing zeros.
    
    Converts a numerical value to a string for labeling the tick increments along an 
    axis in plots. This function removes trailing zeros in numerical values that may
    occur due to floating point precision. For example, a floating point number such as
    
    59.400000000000006
     
    will be returned as a string 
    
    '59.4'
    
    without the trailing insignificant figures.
        
    INPUTS:
    value : value to be displayed at tick increment on axis
    
    OUTPUTS:
    label: string containing number to display below tick increment on axis
    '''
    number_digits = 0
    if not use_sci_notation(value):
        label = str(value)
        
        # Get substring after period
        trailing = label.partition('.')[2]
        number_sigfig = 0
        if len(trailing) > 0:
            # Find number of non-zero digits after decimal
            number_sigfig = 1
            before = trailing[0]
            number_digits = 1
            go = True
            while go and number_digits < len(trailing):
                if trailing[number_digits] == before:
                    number_sigfig = number_digits - 1
                    if(number_sigfig > 5): go = False
                else:
                    before = trailing[number_digits]
                    number_sigfig = number_digits - 1
                number_digits+=1
    
        if number_digits == len(trailing): number_sigfig = number_digits

        # Round up the number to desired significant figures
        label = str(round(value, number_sigfig))
    else:
        label = "{:.1e}".format(value)

    return label
