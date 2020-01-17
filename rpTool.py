#!/usr/bin/env python3

from __future__ import print_function
import argparse
import shutil
import sys
import glob
import os
import csv


import subprocess
import resource
import logging
import glob


# Wrapper for the RP2paths script that takes the same input (results.csv) as the original script but returns
# the out_paths.csv so as to be compliant with Galaxy


MAX_VIRTUAL_MEMORY = 20000*1024*1024 # 20 GB -- define what is the best

##
#
#
def limit_virtual_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))


##
# Although it may seem better to call the RP2path.py script directly, 
#
def run_rp2paths(rp_results, timeout, tmpOutputFolder, out_paths, out_compounds):
    try:
        rp2paths_command = 'python /src/RP2paths.py all '+str(rp_results)+' --outdir '+str(tmpOutputFolder)+' --timeout '+str(timeout)
        commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=limit_virtual_memory)
        try:
            commandObj.wait(timeout=timeout+10.0)
        except subprocess.TimeoutExpired as e:
            logging.error('Timeout from rp2paths ('+str(timeout)+' minutes)')
            commandObj.kill()
            return b'timeout', 'Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
        (result, error) = commandObj.communicate()
        result = result.decode('utf-8')
        error = error.decode('utf-8')
        ### if java has an memory issue
        if 'There is insufficient memory for the Java Runtime Environment to continue' in result:
            logging.error('rp2paths does not have sufficient memory to continue')
            return b'memerror', 'Command: '+str(rp2paths_command)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
    except OSError as e:
        logging.error('Running the rp2paths produced an OSError')
        logging.error(e)
        return b'oserror', 'Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
    except ValueError as e:
        logging.error('Cannot set the RAM usage limit')
        logging.error(e)
        return b'ramerror', 'Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
    shutil.copy2(tmpOutputFolder+'/out_paths.csv', out_paths)
    shutil.copy2(tmpOutputFolder+'/compounds.txt', out_compounds)
    return b'noerror', ''


##
#
#
def main(rp_results, out_paths, out_commands, timeout):
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        status, errorstring = run_rp2paths(rp_results, timeout, tmpOutputFolder, out_paths, out_compounds)


        ### copy the .dat files to .csv and the rules file if need be
        i#sourcefile, fname_source = readCopyFile(sourcefile, tmpOutputFolder)
        s#inkfile, fname_sink = readCopyFile(sinkfile, tmpOutputFolder)
        if (rulesfile==None) or (rulesfile=='None') or (rulesfile==''):
            rulesfile = RULES_PATH
        else:
            rulesfile, fname_rules = readCopyFile(rulesfile, tmpOutputFolder)
        ### run RetroPath2.0
        status, errorstring = run_rp2(sinkfile, sourcefile, maxSteps, rulesfile, scopeCSV, tmpOutputFolder, topx, dmin, dmax, mwmax_source, mwmax_cof, timeout)
        #if the errors are not detected by Galaxy catch them here
        #logging.error(errorstring)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for the python RP2paths script')
    parser.add_argument('-rp_results', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-timeout', type=int)
    parser.add_argument('-out_compounds', type=str)
    #parser.add_argument('-out_scope_csv', type=str)
    params = parser.parse_args()
    tmpOutputFolder = '/src/results'
    exit_code = main(params.rp_results, params.timeout, tmpOutputFolder)
    #print(glob.glob('*_scope.csv'))
    #shutil.copy2(tmpOutputFolder+'/'+glob.glob('*_scope.csv')[0], params.out_scope_csv)
    exit(exit_code)
