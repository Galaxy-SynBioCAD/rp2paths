FROM conda/miniconda3

WORKDIR /home/

# Although graphviz is also in conda, it depends on X11 libraries in /usr/lib
# which this Docker image does not have.
# We'll sacrifize space for a duplicate install to get all the dependencies
# Tip: openjdk-8-jre needed to launch efm
# debian security updates as conda/miniconda3:latest is seldom updated
RUN apt-get --quiet update && \
    apt-get --quiet --yes install \
        ca-certificates \
        build-essential \
        curl \
        wget \
        xz-utils \
        graphviz \
        openjdk-8-jre \
        libxext6  \
        libxrender-dev

RUN conda install -y -c rdkit rdkit
RUN conda update -n base -c defaults conda
RUN conda install -c conda-forge flask-restful
#RUN conda install -y -c rdkit/label/attic rdkit
RUN conda install --quiet --yes python-graphviz pydotplus lxml


###### REDIS ######

RUN apt-get --quiet --yes install supervisor redis-server
RUN conda install -c anaconda redis
RUN conda install -c conda-forge rq

###### Files ####

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY supervisor.conf /home/
COPY start.sh /home/

RUN chmod +x /home/start.sh
CMD ["/home/start.sh"]

# Open server port
EXPOSE 8888
