#FROM scratch as cwl
#COPY /tools /usr/share/cwl/rp2paths
#LABEL org.w3id.cwl.tool /usr/share/cwl/rp2paths/rp2paths.cwl

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


RUN mkdir /src

COPY flask_rq.py /src/
COPY start.sh /src/
COPY rp2paths.py /src/
COPY supervisor.conf /src/

RUN chmod +x /src/start.sh

CMD ["/src/start.sh"]

EXPOSE 8992
