#!/usr/bin/env python3

from __future__ import print_function
import argparse
import subprocess
import shutil
import glob
import os
import csv

import sys
sys.path.insert(0, '/src/')
import rpTool

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp_results', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-out_compounds', type=str)
    parser.add_argument('-timeout', type=int)
    params = parser.parse_args()
    rpTool.main(params.rp_results, params.out_paths, params.out_compounds, params.timeout)
