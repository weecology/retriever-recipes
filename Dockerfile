FROM ubuntu:18.04

MAINTAINER Weecology "https://github.com/weecology/retriever"

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Manually install tzdata to allow for non-interactive install
RUN apt-get install -y --force-yes tzdata

RUN apt-get install -y --force-yes build-essential wget git locales locales-all > /dev/null
RUN apt-get install -y --force-yes postgresql-client > /dev/null

# Set encoding
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Remove python2 and install python3
RUN apt-get remove -y python && apt-get install -y python3  python3-pip curl
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
RUN rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

RUN echo "export PATH="/usr/bin/python:$PATH"" >> ~/.profile
RUN echo "export PYTHONPATH="/usr/bin/python:$PYTHONPATH"" >> ~/.profile
RUN echo "export PGPASSFILE="~/.pgpass"" >> ~/.profile

# Add permissions to config files
RUN chmod 0644 ~/.profile

# Install requirements
RUN pip3 install psycopg2-binary
RUN pip3 install pytest
RUN pip3 install h5py
RUN pip3 install Pillow
RUN pip3 install kaggle
RUN pip3 install git+https://git@github.com/weecology/retriever.git

# Install Postgis after Python is setup
RUN apt-get install -y --force-yes postgis

COPY . ~/recipes
WORKDIR ~/recipes
