#!/bin/sh

#docker run --network host -d -p 8888:8888 --name test_rp2paths brsynth/rp2paths-rest
docker run -d -p 8888:8888 --name test_rp2paths brsynth/rp2paths-rest
sleep 10
python tool_rp2paths.py -rp2_pathways test_rp2_pathways.csv -rp2paths_pathways output_outPaths.csv -rp2paths_compounds output_outCompounds.csv -timeout 18000 -server_url http://0.0.0.0:8888/REST
docker kill test_rp2paths
docker rm test_rp2paths
