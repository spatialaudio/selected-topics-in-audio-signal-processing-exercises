FROM andrewosh/binder-base

MAINTAINER Matthias Geier <Matthias.Geier@gmail.com>

USER root

# install OS packages
RUN apt-get update
RUN apt-get install -y libsndfile1 sndfile-programs sox libsox-fmt-all
RUN apt-get install -y vorbis-tools

USER main

# install Python libraries
RUN pip install soundfile
RUN $HOME/anaconda2/envs/python3/bin/pip install soundfile
RUN pip install sfs
RUN $HOME/anaconda2/envs/python3/bin/pip install sfs
