#!/bin/bash

docker run -v ${PWD}/test_rp2_pathways.csv:/home/test_rp2_pathways.csv -v ${PWD}/tool_rp2paths.py:/home/tool_rp2paths.py -v ${PWD}/out_results/:/home/out_results/ -v ${PWD}/inside_run.sh:/home/inside_run.sh --rm brsynth/rp2paths /bin/sh /home/inside_run.sh

cp out_results/output_outPaths.csv .
cp out_results/output_outCompounds.csv .
