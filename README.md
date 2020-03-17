# rp2paths docker

* Docker image: [brsynth/retroapth2-redis](https://hub.docker.com/r/brsynth/retropath2-redis)

RP2paths extracts the set of pathways that lies in a metabolic space file output by the RetroPath2.0 workflow. Source code may be found at the following location: [GitHub](https://github.com/brsynth/rp2paths).

## Input

Required information: 
* **rp_results**: (string) Path to the ReatroPath2.0 pathways file

Advanced options: 
* **timeout**: (string, default: 30 minutes) Time out time of the tool
* **server_url**: (string) IP address of the rp2paths REST service

## Output

* **out_paths**: (string) Path to the RP2paths pathways. Describes all the indiviudal enumerated pathways that produce the compound of interest.
* **out_compounds**: (string) Path to the RP2paths Compounds. Describes the structure of all the chemical species involved in all pathways.

## Building the docker

To build the docker, please run the following command in the project root folder:

```
docker build -t brsynth/rp2paths-redis .
```

To run the rest/redis service:

```
docker run docker run -p 8888:8888 brsynth/rp2paths-redis:dev
```

### Running the tests

To run the test, first untar the test.tar.xz folder and run the following command:

```
python tool_rp2paths.py -rp2_pathways test/rp2_pathways.csv -rp2paths_pathways test/out_paths.csv -rp2paths_compounds test/out_compounds.csv -server_url http://0.0.0.0:8888/REST
```

## Dependencies

* Base docker image: [conda/miniconda3](https://hub.docker.com/r/conda/miniconda3)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v0.1

## Authors

* **Melchior du Lac**
* Thomas Duigou
* Baudoin Delépine
* Pablo Carbonell

## License

[MIT](https://github.com/brsynth/rp2paths/blob/master/LICENSE.txt)

## Acknowledgments

* Joan Hérisson

### How to cite rp2paths?

Delépine B, Duigou T, Carbonell P, Faulon JL. RetroPath2.0: A retrosynthesis workflow for metabolic engineers. Metabolic Engineering, 45: 158-170, 2018. DOI: https://doi.org/10.1016/j.ymben.2017.12.002
