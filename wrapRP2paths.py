#!/usr/bin/env python3

from __future__ import print_function
import argparse
import subprocess
import shutil
import sys
import glob
import os
import csv

# Wrapper for the RP2paths script that takes the same input (results.csv) as the original script but returns
# the out_paths.csv so as to be compliant with Galaxy

#Debug function
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#Although it may seem better to call the RP2path.py script directly, 
def main(rp_results, timeout, outDir):
    rp2paths_command = ['python', '/src/RP2paths.py', 'all', rp_results, '--outdir', outDir, '--timeout', str(timeout)]
    try:
        #exit_code = subprocess.call(rp2paths_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        #exit_code = subprocess.call(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = subprocess.call(rp2paths_command)
    except OSError as e:
        eprint('ERROR: subprocess detected an error when calling the rp2paths command')
        return 2
    return exit_code


#function that takes the .dat input of a file, opens to be read by python and then writes it to a CSV file
def readCopyFile(inputFile, outDir):
    #outputFile = outDir+'/'+inputFile.split('/')[-1].replace('.dat', '')+'.csv'
    outputFile = inputFile.split('/')[-1].replace('.dat', '')+'.csv' 
    with open(outputFile, 'w') as outF:
        outCSV = csv.writer(outF, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        with open(inputFile, 'r') as inF:
            inCSV = csv.reader(inF, delimiter=',', quotechar='"')
            for row in inCSV:
                outCSV.writerow(row)
    return outputFile, inputFile.split('/')[-1].replace('.dat', '')+'.csv'


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp_results', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-timeout', type=int)
    parser.add_argument('-out_compounds', type=str)
    #parser.add_argument('-out_scope_csv', type=str)
    params = parser.parse_args()
    outDir = '/src/results'
    exit_code = main(params.rp_results, params.timeout, outDir)
    shutil.copy2(outDir+'/out_paths.csv', params.out_paths)
    shutil.copy2(outDir+'/compounds.txt', params.out_compounds)
    #print(glob.glob('*_scope.csv'))
    #shutil.copy2(outDir+'/'+glob.glob('*_scope.csv')[0], params.out_scope_csv)
    exit(exit_code)
