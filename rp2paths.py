#!/usr/bin/env python3
"""
Created on March 7 2019

@author: Melchior du Lac
@description: RQ version of RP2paths

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import io
import json
import time
import os
import random
import string
import subprocess
import logging
import resource
import tempfile

MAX_VIRTUAL_MEMORY = 15000 * 1024 * 1024 # 15 GB -- define what is the best

def limit_virtual_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

def run(rp2_pathways_bytes, timeout):
    out_paths = b''
    out_compounds = b''
    with tempfile.TemporaryDirectory() as tmpFolder:
        rp2_pathways = tmpFolder+'/tmp_rp2_pathways.csv'
        with open(tmpFolder+'/tmp_rp2_pathways.csv', 'rb') as outfi:
            outfi.write(rp2_pathways_bytes)
        rp2paths_command = ['python', '/home/RP2paths.py', 'all', rp2_pathways, '--outdir', tmpFolder, '--timeout', str(timeout)]
        try:
            commandObj = subprocess.Popen(rp2paths_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, preexec_fn=limit_virtual_memory)
            commandObj.wait()
            (result, error) = commandObj.communicate()
            result = result.decode('utf-8')
            error = error.decode('utf-8')
            if 'There is insufficient memory for the Java Runtime Environment to continue' in result:
                logging.error('RP2paths does not have sufficient memory to continue')
                oout_path = b''
                out_compounds = b''
            ### convert the result to binary and return ###
            try:
                with open(tmpFolder+'/out_paths.csv', 'rb') as op:
                    out_paths = op.read()
                with open(tmpFolder+'/compounds.txt', 'rb') as c:
                    out_compounds = c.read()
            except FileNotFoundError:
                logging.error('Cannot find the output files out_paths.csv or compounds.txt')
        except OSError as e:
            logging.error('Subprocess detected an error when calling the rp2paths command')
        except ValueError as e:
            logging.error('Cannot set the RAM usage limit')
            logging.error(e)
    return out_paths, out_compounds
