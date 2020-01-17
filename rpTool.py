"""
Created on March 7 2019

@author: Melchior du Lac
@description: RQ version of RP2paths

"""
import subprocess
import logging
import resource
import tempfile
import glob

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
        rp2paths_command = 'python /data/RP2paths.py all '+str(rp2_pathways)+' --outdir '+str(tmpOutputFolder)+' --timeout '+str(timeout)
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
                return b'', b'', b'memoryerror'
            ### convert the result to binary and return ###
            try:
                with open(tmpOutputFolder+'/out_paths.csv', 'rb') as op:
                    out_paths = op.read()
                with open(tmpOutputFolder+'/compounds.txt', 'rb') as c:
                    out_compounds = c.read()
                return out_paths, out_compounds, b''
            except FileNotFoundError:
                logging.error('Cannot find the output files out_paths.csv or compounds.txt')
                return b'', b'', b'filenotfounderror'
        except OSError as e:
            logging.error('Subprocess detected an error when calling the rp2paths command')
            return b'', b'', b'oserror'
        except ValueError as e:
            logging.error('Cannot set the RAM usage limit')
            return b'', b'', b'valueerror'
    return out_paths, out_compounds, b''



##
#
#
def main(rp2_pathways, timeout):
    with open(rp2_pathways, 'rb') as rp2_pathways_bytes:
        result = run_rp2paths(rp2_pathways_bytes, timeout)
        #app.logger.info(result)
        if result[2]==b'filenotfounderror':
            logging.error('FileNotFound Error from rp2paths')
            return False
        elif result[2]==b'oserror':
            logging.error('rp2paths has generated an OS error')
            return False
        elif result[2]==b'memerror':
            logging.error(' Memory allocation error')
            return False
        elif result[0]==b'' and result[1]==b'':
            logging.error('Could not find any results by RetroPath2.0')
            return False
        elif result[2]==b'valueerror':
            logging.error('Could not setup a RAM limit')
            return False
        out_paths = io.BytesIO(result[0])
        out_compounds = io.BytesIO(result[1])
        return out_paths, out_compounds
