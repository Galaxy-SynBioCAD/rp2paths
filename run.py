#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Extract the sink from an SBML into RP2 friendly format

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker

import glob

##
#
#
def main(rp_pathways, rp2paths_pathways, rp2paths_compounds, timeout=30, max_steps=0):
    docker_client = docker.from_env()
    image_str = 'brsynth/rp2paths-standalone'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        shutil.copy(rp_pathways, tmpOutputFolder+'/rp_pathways.csv')
        command = ['python',
                   '/home/tool_rp2paths.py',
                   '-rp_pathways',
                   '/home/tmp_output/rp_pathways.csv',
                   '-rp2paths_compounds',
                   '/home/tmp_output/rp2paths_compounds.csv',
                   '-rp2paths_pathways',
                   '/home/tmp_output/rp2paths_pathways.csv',
                   '-timeout',
                   str(timeout),
                   '-max_steps',
                   str(max_steps)]
        container = docker_client.containers.run(image_str, 
                                                 command, 
                                                 detach=True,
                                                 stderr=True,
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        err_str = err.decode('utf-8')
        if not 'ERROR' in err_str:
            shutil.copy(tmpOutputFolder+'/rp2paths_pathways.csv', rp2paths_pathways)
            shutil.copy(tmpOutputFolder+'/rp2paths_compounds.csv', rp2paths_compounds)
        else:
            print(err_str)
        container.remove()





##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Enumerate the individual pathways from the results of Retropath2')
    parser.add_argument('-rp_pathways', type=str)
    parser.add_argument('-rp2paths_pathways', type=str)
    parser.add_argument('-rp2paths_compounds', type=str)
    parser.add_argument('-max_steps', type=int, default=0)
    parser.add_argument('-timeout', type=int, default=30)
    params = parser.parse_args()
    if params.timeout<0:
        logging.error('Timeout cannot be <0 :'+str(params.timeout))
        exit(1)
    main(params.rp_pathways, params.rp2paths_pathways, params.rp2paths_compounds, params.timeout, params.max_steps)
