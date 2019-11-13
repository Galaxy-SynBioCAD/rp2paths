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
    apt-get --quiet --yes install supervisor redis && \
    apt-get --quiet --yes install \
        curl \
        graphviz \
        openjdk-8-jre 

RUN pip install rq redis

## Install rest of dependencies as Conda packages
# Update conda base install in case base Docker image is outdated
# Install rdkit first as it has loads of dependencies
# Check for new versions at
# https://anaconda.org/rdkit/rdkit/labels
# FIXME: Is it pip's image or conda's scikit-image?
#RUN pip install -y image
#conda install scikit-image
RUN conda update --quiet --yes conda && \
    conda update --all --yes && \
    conda install -c conda-forge flask-restful && \
    conda install --quiet --yes python-graphviz pydotplus lxml


# Download and "install" rp2paths release
RUN mkdir /home/
WORKDIR /home/
RUN echo "$RP2PATHS_SHA256  rp2paths.tar.gz" > rp2paths.tar.gz.sha256
RUN cat rp2paths.tar.gz.sha256
RUN echo Downloading $RP2PATHS_URL
RUN curl -v -L -o rp2paths.tar.gz $RP2PATHS_URL && sha256sum rp2paths.tar.gz && sha256sum -c rp2paths.tar.gz.sha256
RUN tar xfv rp2paths.tar.gz && mv rp2paths*/* /home/
RUN grep -q '^#!/' RP2paths.py || sed -i '1i #!/usr/bin/env python3' RP2paths.py

RUN mkdir /home/data
RUN mkdir /home/results

WORKDIR /home/

COPY rp2paths.py /home/
COPY supervisor.conf /home/
COPY flask_rq.py /home/
COPY start.sh /home/

RUN chmod +x /home/start.sh

CMD ["/home/start.sh"]

EXPOSE 8992
