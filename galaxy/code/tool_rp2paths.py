#!/usr/bin/env python3

import argparse
import sys
import logging

sys.path.insert(0, '/home/')
import rpTool

logging.basicConfig(
    #level=logging.DEBUG,
    level=logging.WARNING,
    #level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)

# Wrapper for the RP2paths script that takes the same input (results.csv) as the original script but returns
# the out_paths.csv so as to be compliant with Galaxy
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp_pathways', type=str)
    parser.add_argument('-rp2paths_pathways', type=str)
    parser.add_argument('-rp2paths_compounds', type=str)
    parser.add_argument('-timeout', type=int, default=30)
    params = parser.parse_args()
    if params.timeout<=0:
        logging.error('Timeout cannot be less or equal to 0 :'+str(params.timeout))
        exit(1)
    result = rpTool.run_rp2paths(params.rp_pathways, params.timeout)
    if result[2]==b'timeout':
        logging.error('RP2paths has reached its timeout limit')
        exit(1)
    if result[2]==b'filenotfounderror':
        logging.error('Cannot detect the out_path.csv and/or compounds.txt files')
        exit(1)
    elif result[2]==b'memoryerror':
        logging.error('Memory allocation error')
        exit(1)
    elif result[2]==b'oserror':
        logging.error('rp2paths has generated an OS error')
        exit(1)
    elif result[2]==b'ramerror':
        logging.error('Could not setup a RAM limit')
        exit(1)
    elif result[0]==b'':
        logging.error('Empty rp2paths_pathways')
        exit(1)
    elif result[1]==b'':
        logging.error('Empty rp2paths_compounds')
        exit(1)
    with open(params.rp2paths_pathways, 'wb') as out_paths:
        out_paths.write(result[0])
    with open(params.rp2paths_compounds, 'wb') as out_compounds:
        out_compounds.write(result[1])
