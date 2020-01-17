FROM conda/miniconda3

# Although graphviz is also in conda, it depends on X11 libraries in /usr/lib
# which this Docker image does not have.
# We'll sacrifize space for a duplicate install to get all the dependencies
# Tip: openjdk-8-jre needed to launch efm
# debian security updates as conda/miniconda3:latest is seldom updated
RUN apt-get --quiet update && \
    apt-get --quiet --yes dist-upgrade && \
    apt-get --quiet --yes install \
	supervisor \
	redis-server \
        curl \
        graphviz \
        openjdk-8-jre

RUN conda update --quiet --yes conda && conda update --all --yes
RUN conda install --quiet --yes --channel rdkit rdkit=2018.03.4.0
RUN conda install --quiet --yes python-graphviz pydotplus lxml

WORKDIR /src/

###### JOAN: this part is docker_compose I geuss, I need it for testing
# Download and "install" rp2paths release
# Check for new versions from 
# https://github.com/brsynth/rp2paths/releases
ENV RP2PATHS_VERSION 1.0.2
ENV RP2PATHS_URL https://github.com/brsynth/rp2paths/archive/v${RP2PATHS_VERSION}.tar.gz
# NOTE: Update sha256sum for each release
ENV RP2PATHS_SHA256 3813460dea8bb02df48e1f1dfb60751983297520f09cdfcc62aceda316400e66
WORKDIR /tmp/
RUN echo "$RP2PATHS_SHA256  rp2paths.tar.gz" > rp2paths.tar.gz.sha256
RUN cat rp2paths.tar.gz.sha256
RUN echo Downloading $RP2PATHS_URL
RUN curl -v -L -o rp2paths.tar.gz $RP2PATHS_URL && sha256sum rp2paths.tar.gz && sha256sum -c rp2paths.tar.gz.sha256
RUN tar xfv rp2paths.tar.gz && mv rp2paths*/* /src
WORKDIR /src/
RUN grep -q '^#!/' RP2paths.py || sed -i '1i #!/usr/bin/env python3' RP2paths.py

COPY rpTool.py /src/
