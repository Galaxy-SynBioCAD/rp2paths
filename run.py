#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Wrap rp2paths into a docker

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker

import glob

def main(rp_pathways, rp2paths_pathways, rp2paths_compounds, timeout=30, max_steps=0, max_paths=150, unfold_compounds=False):
    """Call the docker to run rp2paths 

    :param rp_pathways: The path to the results RetroPath2.0 scope file
    :param rp2paths_pathways: The path to the results rp2paths out_paths file
    :param rp2paths_compounds: The path to the results rp2paths compounds file
    :param timeout: The timeout of the function in minutes (Default: 90)
    :param max_steps: The maximal number of steps WARNING: not used (Default: 0, ie. infinite)
    :param max_paths: The maximal number of pathways to return WARNING: not used (Default: 150)
    :param unfold_compounds: not sure WARNING: not used (Default: False)

    :param rp_pathways: str
    :param rp2paths_pathways: str 
    :param rp2paths_compounds: str
    :param timeout: int
    :param max_steps: int
    :param max_paths: int
    :param unfold_compounds: bool

    :rtype: None
    :return: None
    """

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
                   str(max_steps),
                   '-max_paths',
                   str(max_paths),
                   '-unfold_compounds',
                   str(unfold_compounds)]
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Enumerate the individual pathways from the results of Retropath2')
    parser.add_argument('-rp_pathways', type=str)
    parser.add_argument('-rp2paths_pathways', type=str)
    parser.add_argument('-rp2paths_compounds', type=str)
    parser.add_argument('-max_steps', type=int, default=0)
    parser.add_argument('-timeout', type=int, default=30)
    parser.add_argument('-max_paths', type=int, default=150)
    parser.add_argument('-unfold_compounds', type=str, default='False')
    params = parser.parse_args()
    if params.timeout<0:
        logging.error('Timeout cannot be <0 :'+str(params.timeout))
        exit(1)
    main(params.rp_pathways, params.rp2paths_pathways, params.rp2paths_compounds, params.timeout, params.max_steps, params.max_paths, params.unfold_compounds)
