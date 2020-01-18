FROM conda/miniconda3

# Although graphviz is also in conda, it depends on X11 libraries in /usr/lib
# which this Docker image does not have.
# We'll sacrifize space for a duplicate install to get all the dependencies
# Tip: openjdk-8-jre needed to launch efm
# debian security updates as conda/miniconda3:latest is seldom updated
RUN apt-get --quiet update && \
    apt-get --quiet --yes dist-upgrade && \
    apt-get --quiet --yes install \
        curl \
        graphviz \
        openjdk-8-jre \
        libxext6  \
        libxrender-dev \
        supervisor

#RUN pip3 install rq redis flask-restful

RUN conda update -n base -c defaults conda
RUN conda install -y -c rdkit rdkit
RUN conda install --quiet --yes python-graphviz pydotplus lxml
RUN conda install -c conda-forge rq
RUN conda install -c anaconda redis
RUN conda install -c conda-forge flask-restful

WORKDIR /home/

###### JOAN: this part is docker_compose I geuss. for dev I need it for testing
# Download and "install" rp2paths release
# Check for new versions from 
# https://github.com/brsynth/rp2paths/releases
ENV RP2PATHS_VERSION 1.0.2
ENV RP2PATHS_URL https://github.com/brsynth/rp2paths/archive/v${RP2PATHS_VERSION}.tar.gz
# NOTE: Update sha256sum for each release
ENV RP2PATHS_SHA256 3813460dea8bb02df48e1f1dfb60751983297520f09cdfcc62aceda316400e66
RUN echo "$RP2PATHS_SHA256  rp2paths.tar.gz" > rp2paths.tar.gz.sha256
RUN cat rp2paths.tar.gz.sha256
RUN echo Downloading $RP2PATHS_URL
RUN curl -v -L -o rp2paths.tar.gz $RP2PATHS_URL && sha256sum rp2paths.tar.gz && sha256sum -c rp2paths.tar.gz.sha256
RUN tar xfv rp2paths.tar.gz && mv rp2paths*/* /home/
RUN grep -q '^#!/' RP2paths.py || sed -i '1i #!/usr/bin/env python3' RP2paths.py

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY start.sh /home/
COPY supervisor.conf /home/

RUN chmod +x /home/start.sh

CMD ["/home/start.sh"]

EXPOSE 8888
