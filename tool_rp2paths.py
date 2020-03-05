#!/usr/bin/env python3

import argparse
import sys
import logging

sys.path.insert(0, '/home/')
import rpTool

# Wrapper for the RP2paths script that takes the same input (results.csv) as the original script but returns
# the out_paths.csv so as to be compliant with Galaxy
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp_results', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-timeout', type=int)
    parser.add_argument('-out_compounds', type=str)
    params = parser.parse_args()
    result = rpTool.run_rp2paths(open(params.rp_results, 'rb').read(), params.timeout)
    if result[0]==b'':
        logging.error('Empty results')
    elif result[1]==b'timeout':
        logging.error.error('Timeout of RetroPath2.0')
    elif result[1]==b'memoryerror':
        logging.error.error('Memory allocation error')
    elif result[1]==b'oserror':
        logging.error.error('rp2paths has generated an OS error')
    elif result[1]==b'ramerror':
        logging.error.error('Could not setup a RAM limit')
    with open(params.out_paths, 'wb') as out_paths:
        out_paths.write(result[0])
    with open(params.out_compounds, 'wb') as out_compounds:
        out_compounds.write(result[1])
