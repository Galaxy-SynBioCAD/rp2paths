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
import logging


logging.basicConfig(
    #level=logging.DEBUG,
    level=logging.WARNING,
    #level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)

MAX_VIRTUAL_MEMORY = 20000 * 1024 * 1024 # 20GB -- define what is the best
#MAX_VIRTUAL_MEMORY = 20 * 1024 * 1024 # 20GB -- define what is the best

##
#
#
def limit_virtual_memory():
    """The function to set the memory limits
    """
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

def run_rp2paths(rp2_pathways, timeout, logger=None):
    """Call the KNIME RetroPath2.0 workflow

    :param rp2_pathways: The path to the RetroPath2.0 scope results
    :param timeout: The timeout of the function in minutes
    :param logger: Logger object (Default: None)

    :param source_bytes: str
    :param sink_bytes: int
    :param logger: logging

    :rtype: tuple
    :return: tuple of bytes with the out_paths results, compounds results, the status message, the command used
    """
    ### not sure why throws an error:
    if logger==None:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
    out_paths = b''
    out_compounds = b''
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        rp2paths_command = 'python /home/RP2paths.py all '+str(rp2_pathways)+' --outdir '+str(tmpOutputFolder)+' --timeout '+str(int(timeout*60.0))
        try:
            commandObj = subprocess.Popen(rp2paths_command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=limit_virtual_memory)
            result = b''
            error = b''
            result, error = commandObj.communicate()
            result = result.decode('utf-8')
            error = error.decode('utf-8')
            #TODO test to see what is the correct phrase
            if 'TIMEOUT' in result:
                logger.error('Timeout from of ('+str(timeout)+' minutes)')
                return b'', b'', b'timeout', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(error)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
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
            return b'', b'', b'ramerror', str.encode('Command: '+str(rp2paths_command)+'\n Error: '+str(e)+'\n tmpOutputFolder: '+str(glob.glob(tmpOutputFolder+'/*')))
