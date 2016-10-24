FROM andrewosh/binder-base

MAINTAINER Fiete Winter <Fiete.Winter@uni-rostock.de>

USER root

# install OS packages
RUN apt-get update
RUN apt-get install -y libsndfile1 sndfile-programs

USER main

# install Python libraries
RUN pip install soundfile
RUN $HOME/anaconda2/envs/python3/bin/pip install soundfile
RUN pip install sfs
RUN $HOME/anaconda2/envs/python3/bin/pip install sfs
