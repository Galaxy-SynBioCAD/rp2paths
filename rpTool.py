"""
Created on March 7 2019

@author: Melchior du Lac
@description: Standalone version of RP2paths. Returns bytes to be able to use the same file in REST application

"""
import subprocess
import logging
import resource
import tempfile
import glob
import io

MAX_VIRTUAL_MEMORY = 20000 * 1024 * 1024 # 20GB -- define what is the best

##
#
#
def limit_virtual_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

##
#
#
def run_rp2paths(rp2_pathways_bytes, timeout):
    out_paths = b''
    out_compounds = b''
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        rp2_pathways = tmpOutputFolder+'/tmp_rp2_pathways.csv'
        with open(tmpOutputFolder+'/tmp_rp2_pathways.csv', 'wb') as outfi:
            outfi.write(rp2_pathways_bytes)
        #rp2paths_command = ['python', '/home/RP2paths.py', 'all', rp2_pathways, '--outdir', tmpOutputFolder, '--timeout', str(timeout)]
        rp2paths_command = 'python /home/RP2paths.py all '+str(rp2_pathways)+' --outdir '+str(tmpOutputFolder)+'/ --timeout '+str(timeout)
        try:
            commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=limit_virtual_memory)
            #commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, preexec_fn=limit_virtual_memory)
            commandObj.wait()
            (result, error) = commandObj.communicate()
            result = result.decode('utf-8')
            error = error.decode('utf-8')
            #TODO test to see what is the correct phrase
            if 'failed to map segment from shared object' in error:
                logging.error('RP2paths does not have sufficient memory to continue')
                return b'', b'', b'memoryerror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(error)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
            ### convert the result to binary and return ###
            try:
                with open(tmpOutputFolder+'/out_paths.csv', 'rb') as op:
                    out_paths = op.read()
                with open(tmpOutputFolder+'/compounds.txt', 'rb') as c:
                    out_compounds = c.read()
                return out_paths, out_compounds, b'noerror', b''
            except FileNotFoundError as e:
                logging.error('Cannot find the output files out_paths.csv or compounds.txt')
                return b'', b'', b'filenotfounderror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
        except OSError as e:
            logging.error('Subprocess detected an error when calling the rp2paths command')
            return b'', b'', b'oserror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
        except ValueError as e:
            logging.error('Cannot set the RAM usage limit')
            return b'', b'', b'valueerror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))



##
#
#
def main(rp2_pathways_bytes, timeout):
    result = run_rp2paths(rp2_pathways_bytes, timeout)
    #app.logger.info(result)
    if result[2]==b'filenotfounderror':
        logging.error('FileNotFound Error from rp2paths')
        logging.error(result[3])
        return b'', b''
    elif result[2]==b'oserror':
        logging.error('rp2paths has generated an OS error')
        logging.error(result[3])
        return b'', b''
    elif result[2]==b'memerror':
        logging.error('Memory allocation error')
        logging.error(result[3])
        return b'', b''
    elif result[0]==b'' and result[1]==b'':
        logging.error('Could not find any results')
        logging.error(result[3])
        return b'', b''
    elif result[2]==b'valueerror':
        logging.error('Could not setup a RAM limit')
        logging.error(result[3])
        return b'', b''
    out_paths = io.BytesIO(result[0])
    out_compounds = io.BytesIO(result[1])
    return out_paths, out_compounds
