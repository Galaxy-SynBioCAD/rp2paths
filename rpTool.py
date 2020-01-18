"""
Created on March 7 2019

@author: Melchior du Lac
@description: Standalone version of RP2paths. Returns bytes to be able to use the same file in REST application

"""
import subprocess
import resource
import tempfile
import glob
import io

MAX_VIRTUAL_MEMORY = 20000 * 1024 * 1024 # 20GB -- define what is the best
#MAX_VIRTUAL_MEMORY = 20 * 1024 * 1024 # 20GB -- define what is the best

##
#
#
def limit_virtual_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

##
#
#
def run_rp2paths(rp2_pathways_bytes, timeout, logger):
    out_paths = b''
    out_compounds = b''
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        rp2_pathways = tmpOutputFolder+'/tmp_rp2_pathways.csv'
        with open(tmpOutputFolder+'/tmp_rp2_pathways.csv', 'wb') as outfi:
            outfi.write(rp2_pathways_bytes)
        #rp2paths_command = ['python', '/home/RP2paths.py', 'all', rp2_pathways, '--outdir', tmpOutputFolder, '--timeout', str(timeout)]
        rp2paths_command = 'python /home/RP2paths.py all '+str(rp2_pathways)+' --outdir '+str(tmpOutputFolder)+' --timeout '+str(int(timeout*60.0*60.0+10.0))
        try:
            commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=limit_virtual_memory)
            #commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, preexec_fn=limit_virtual_memory)
            try:
                commandObj.wait(timeout=timeout*60.0)
            except subprocess.TimeoutExpired as e:
                logger.error('Timeout from rp2paths ('+str(timeout)+' minutes)')
                commandObj.kill()
                return b'', b'', b'timeout', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpfolder: '+str(glob.glob(tmpfolder+'/*')))
            (result, error) = commandObj.communicate()
            result = result.decode('utf-8')
            error = error.decode('utf-8')
            #TODO test to see what is the correct phrase
            if 'failed to map segment from shared object' in error:
                logger.error('RP2paths does not have sufficient memory to continue')
                return b'', b'', b'memoryerror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(error)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
            ### convert the result to binary and return ###
            try:
                with open(tmpOutputFolder+'/out_paths.csv', 'rb') as op:
                    out_paths = op.read()
                with open(tmpOutputFolder+'/compounds.txt', 'rb') as c:
                    out_compounds = c.read()
                return out_paths, out_compounds, b'noerror', b''
            except FileNotFoundError as e:
                logger.error('Cannot find the output files out_paths.csv or compounds.txt')
                return b'', b'', b'filenotfounderror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
        except OSError as e:
            logger.error('Subprocess detected an error when calling the rp2paths command')
            return b'', b'', b'oserror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
        except ValueError as e:
            logger.error('Cannot set the RAM usage limit')
            return b'', b'', b'valueerror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
