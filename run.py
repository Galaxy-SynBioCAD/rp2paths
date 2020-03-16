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


##
#
#
def main(rp_results, out_paths, out_compounds, timeout):
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
        shutil.copy(rp_results, tmpOutputFolder+'/rp_results.csv')
        command = ['/home/tool_rp2paths.py',
                   '-rp_results',
                   '/home/tmp_output/rp_results.csv',
                   '-out_compounds',
                   '/home/tmp_output/out_compounds.csv',
                   '-out_paths',
                   '/home/tmp_output/out_paths.csv',
                   '-timeout',
                   str(timeout)]
        container = docker_client.containers.run(image_str, 
                                                 command, 
                                                 detach=True,
                                                 stderr=True,
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        print(err)
        shutil.copy(tmpOutputFolder+'/out_paths.csv', out_paths)
        shutil.copy(tmpOutputFolder+'/out_compounds.csv', out_compounds)
        container.remove()





##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Enumerate the individual pathways from the results of Retropath2')
    parser.add_argument('-rp_results', type=str)
    parser.add_argument('-out_paths', type=str)
    parser.add_argument('-out_compounds', type=str)
    parser.add_argument('-timeout', type=int, default=30)
    params = parser.parse_args()
    main(params.rp_results, params.out_paths, params.out_compounds, params.timeout)
