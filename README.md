# rp2paths

* Docker image: [brsynth/rp2paths](https://hub.docker.com/r/brsynth/rp2paths-standalone)

Docker implementation of rp2paths. Enumerates individual heterologous pathways from RetroPath2.0.

## Input

Required:
* **-rp_results**: (string) Path to the output of RetroPath2.0 

Advanced options:
* **-timeout**: (integer, default=30) Timeout of the tool in minutes

## Output

* **-out_paths**: (string) Path to the metabolic pathways calculated
* **-out_compounds**: (string) Path to the compounds in the calculated pathways

## Dependencies

* Base docker image: [conda/miniconda3](https://hub.docker.com/r/conda/miniconda3/dockerfile)

## Building the docker

To build the docker, please run the following command command in the project root folder:

```
docker build -t brsynth/rp2paths-standalone .
```

#### Running the test

To test the docker, untar the test.tar.xz file and run the following command:

```
python run.py -rp_pathways test/rp_pathways.csv -rp2paths_pathways test/out_paths.csv -rp2paths_compounds test/out_compounds.csv
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Version

v1.1.0

## Authors

* **Thomas Duigou**
* Joan Hérisson

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

### How to cite rp2paths?
Please cite:

Delépine B, Duigou T, Carbonell P, Faulon JL. RetroPath2.0: A retrosynthesis workflow for metabolic engineers. Metabolic Engineering, 45: 158-170, 2018. DOI: https://doi.org/10.1016/j.ymben.2017.12.002
