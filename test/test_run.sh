#!/bin/bash

docker run -v ${PWD}/test_rp2_pathways.csv:/src/test_rp2_pathways.csv -v ${PWD}/tool_rp2paths.py:/src/tool_rp2paths.py -v ${PWD}/out_results/:/src/out_results/ -v ${PWD}/inside_run.sh:/src/inside_run.sh  --rm brsynth/rp2paths /bin/sh /src/inside_run.sh

cp out_results/output_outPaths.csv .
cp out_results/output_outCompounds.csv .
