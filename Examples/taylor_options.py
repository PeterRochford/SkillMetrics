'''
Simple program to provide list of options for creating a Taylor diagram. Used for package
development. Explicitly accesses the latest method rather than the one distributed in the 
package.

Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com

Created on Apr 22, 2017

@author: prochford@thesymplectic.com
'''
from imp import load_source
        
if __name__ == '__main__':
    # Obtain options for creating Taylor diagram by calling method without arguments
    module = load_source('taylor_diagram','../skill_metrics/taylor_diagram.py')
    module.taylor_diagram()
