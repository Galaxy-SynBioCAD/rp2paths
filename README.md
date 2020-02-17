# rp2paths

RP2paths extracts the set of pathways that lies in a metabolic space file outputed by the RetroPath2.0 workflow. Source code may be found at the following location: [myExperiment.org](https://www.myexperiment.org/workflows/4987.html).

## Information Flow

### Input

Required information: 
    * RetroPath2.0 list of pathways CSV file output.

Advanced options: 
    * TimeOut: (default: 1800 seconds) Time out of the tool
    * Server URL: IP address of the rp2paths REST service

### Output

* RP2paths Pathways: describing all the indiviudal enumerated pathways that produce the compound of interest.
* RP2paths Compounds: describes the structure of all the chemical species involved in all the individual pathways.

## Installing

Compile the docker using the Dockerfile using the following command:

```
docker build -t brsynth/rp2paths-redis:dev .
```

The REST service may be started on the localhost with the following command:

```
docker run -p 8887:8888 brsynth/rp2paths-redis
```

### Prerequisites

* Docker - [Install](https://docs.docker.com/v17.09/engine/installation/)

## Contributing

TODO

## Versioning

Version 0.1

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
