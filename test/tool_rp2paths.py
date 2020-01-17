#!/usr/bin/env python3

import argparse
import shutil
import sys
sys.path.insert(0, '/src/')
import rpTool

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp2_pathways', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-out_compounds', type=str)
    parser.add_argument('-timeout', type=int)
    params = parser.parse_args()
    out_paths, out_compounds = rpTool.main(params.rp2_pathways, params.timeout)
    with open(params.out_paths, 'wb') as o_p:
        o_p.write(out_paths)
    with open(params.out_compounds, 'wb') as o_c:
        o_c.write(out_compounds)
