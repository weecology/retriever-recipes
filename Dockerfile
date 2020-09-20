# Download base image ubuntu 18.04
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Manually install tzdata to allow for non-interactive install
RUN apt-get install -y --force-yes tzdata

RUN apt-get install -y --force-yes build-essential wget git locales locales-all > /dev/null
RUN apt-get install -y --force-yes postgresql-client > /dev/null

# Install python3
RUN apt-get install -y python3 python3-pip curl

# Install requirements
RUN pip3 install psycopg2-binary pytest h5py Pillow kaggle
RUN pip3 install git+https://git@github.com/weecology/retriever.git

# Install Postgis after Python is setup
RUN apt-get install -y --force-yes postgis

COPY . ~/recipes
WORKDIR ~/recipes
