#!/usr/bin/env python3

import subprocess
import shutil
import resource
import logging
import glob
import tempfile

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
def run_rp2paths(rp_results, timeout, tmpOutputFolder):
    try:
        rp2paths_command = 'python /src/RP2paths.py all '+str(rp_results)+' --outdir '+str(tmpOutputFolder)+' --timeout '+str(timeout)
        commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=limit_virtual_memory)
        try:
            commandObj.wait(timeout=timeout+10.0)
        except subprocess.TimeoutExpired as e:
            logging.error('Timeout from rp2paths ('+str(timeout)+' minutes)')
            commandObj.kill()
            return b'', b'', b'timeout', 'Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
        (result, error) = commandObj.communicate()
        result = result.decode('utf-8')
        error = error.decode('utf-8')
        ### if java has an memory issue
        if 'There is insufficient memory for the Java Runtime Environment to continue' in result:
            logging.error('rp2paths does not have sufficient memory to continue')
            return b'', b'', b'memerror', 'Command: '+str(rp2paths_command)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
    except OSError as e:
        logging.error('Running the rp2paths produced an OSError')
        logging.error(e)
        return b'', b'', b'oserror', 'Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
    except ValueError as e:
        logging.error('Cannot set the RAM usage limit')
        logging.error(e)
        return b'', b'', b'ramerror', 'Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*'))
    return str.encode(tmpOutputFolder+'/out_paths.csv'), str.encode(tmpOutputFolder+'/compounds.txt'), b'noerror', ''


##
#
#
def main(rp_results, out_paths, out_compounds, timeout):
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        bytes_out_paths, bytes_out_compounds, status, errorstring = run_rp2paths(rp_results, timeout, tmpOutputFolder)
        shutil.copy2(bytes_out_paths.decode(), out_paths)
        shutil.copy2(bytes_out_compounds.decode(), out_compounds)
        #see if you nee`d to catch the error
