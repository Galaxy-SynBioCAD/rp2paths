# rp2paths docker 

* Docker image: [brsynth/rp2paths](https://hub.docker.com/r/brsynth/rp2paths-standalone/)

Docker implementation of the rp2paths pathway enumeration pathway.

### Build the docker

To build the docker from the DockerFile, in the root folder of the project run the following command:o

```
docker build -t brsynth/rp2paths-standalone:dev .
```

#### Running the test

To test extract the test.tar.xz archive and run the following command in the 

```
python run.py -rp_results test/rp_pathways.csv -out_paths test/out_paths.csv -out_compounds test/out_compounds.csv
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Version 0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson

### How to cite rp2paths?
Please cite:

Delépine B, Duigou T, Carbonell P, Faulon JL. RetroPath2.0: A retrosynthesis workflow for metabolic engineers. Metabolic Engineering, 45: 158-170, 2018. DOI: https://doi.org/10.1016/j.ymben.2017.12.002
