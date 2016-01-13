FROM andrewosh/binder-base

MAINTAINER Matthias Geier <Matthias.Geier@gmail.com>

USER root

# install OS packages
RUN apt-get update
RUN apt-get install -y libsndfile1

USER main

# install Python libraries
RUN pip install soundfile
RUN /home/main/anaconda/envs/python3/bin/pip install soundfile
RUN pip install sfs
RUN /home/main/anaconda/envs/python3/bin/pip install sfs
