#!/bin/bash

python tool_rp2paths.py -rp2_pathways test_rp2_pathways.csv -out_paths output_outPaths.csv -out_compounds output_outCompounds.csv -timeout 18000 

mv output_outPaths.csv /home/out_results/
mv output_outCompounds.csv /home/out_results/
