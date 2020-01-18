#!/usr/bin/env python3

import argparse
#import shutil
import logging
import sys
sys.path.insert(0, '/home/')
import rpTool

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp2_pathways', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-out_compounds', type=str)
    parser.add_argument('-timeout', type=int)
    params = parser.parse_args()
    with open(params.rp2_pathways, 'rb') as rp2_pathways_bytes:
        result = rpTool.run_rp2paths(rp2_pathways_bytes.read(), params.timeout, logger)
        with open(params.out_paths, 'wb') as o_p:
            #shutil.copyfileobj(result[0], o_p, length=131072)
            o_p.write(result[0])
        with open(params.out_compounds, 'wb') as o_c:
            #shutil.copyfileobj(result[1], o_c, length=131072)
            o_c.write(result[1])
