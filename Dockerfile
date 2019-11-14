#FROM scratch as cwl
#COPY /tools /usr/share/cwl/rp2paths 
#LABEL org.w3id.cwl.tool /usr/share/cwl/rp2paths/rp2paths.cwl
 
FROM conda/miniconda3
# Check for new versions from 
# https://github.com/brsynth/rp2paths/releases
ENV RP2PATHS_VERSION 1.0.2
ENV RP2PATHS_URL https://github.com/brsynth/rp2paths/archive/v${RP2PATHS_VERSION}.tar.gz
# NOTE: Update sha256sum for each release
ENV RP2PATHS_SHA256 3813460dea8bb02df48e1f1dfb60751983297520f09cdfcc62aceda316400e66

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
#        libxext6  \
#        libxrender-dev \
        openjdk-8-jre 

## Install rest of dependencies as Conda packages
# Update conda base install in case base Docker image is outdated
# Install rdkit first as it has loads of dependencies
# Check for new versions at
# https://anaconda.org/rdkit/rdkit/labels
# FIXME: Is it pip's image or conda's scikit-image?
#RUN pip install -y image
#conda install scikit-image
#RUN conda update --quiet --yes conda && \
#    conda update --all --yes && \
#    conda install -c conda-forge flask-restful && \
#    conda install --quiet --yes python-graphviz pydotplus lxml && \
#    conda install --quiet --yes --channel rdkit rdkit=2018.03.4.0 && \
#    conda install -c conda-forge rq && \
#    conda install -c anaconda redis && \
#    conda install pandas

RUN conda update --quiet --yes conda && conda update --all --yes
RUN conda install --quiet --yes --channel rdkit rdkit=2018.03.4.0
RUN conda install --quiet --yes python-graphviz pydotplus lxml 
RUN conda install -c conda-forge rq
RUN conda install -c anaconda redis
RUN conda install -c conda-forge flask-restful

# Download and "install" rp2paths release
WORKDIR /tmp
RUN echo "$RP2PATHS_SHA256  rp2paths.tar.gz" > rp2paths.tar.gz.sha256
RUN cat rp2paths.tar.gz.sha256
RUN echo Downloading $RP2PATHS_URL
RUN curl -v -L -o rp2paths.tar.gz $RP2PATHS_URL && sha256sum rp2paths.tar.gz && sha256sum -c rp2paths.tar.gz.sha256
RUN mkdir /src
RUN tar xfv rp2paths.tar.gz && mv rp2paths*/* /src
WORKDIR /src
RUN grep -q '^#!/' RP2paths.py || sed -i '1i #!/usr/bin/env python3' RP2paths.py

#RUN mkdir /home/src
#RUN mkdir /home/src/data
RUN mkdir /src/data
RUN mkdir /src/results
RUN chmod -R 755 /src/results

#VOLUME /src

COPY flask_rq.py /src/
COPY start.sh /src/
COPY rp2paths.py /src/
COPY supervisor.conf /src/

RUN chmod +x /src/start.sh

CMD ["/src/start.sh"]

EXPOSE 8992
