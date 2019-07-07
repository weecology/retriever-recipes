# Download base image ubuntu 16.04
FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y --force-yes build-essential wget git locales locales-all > /dev/null
RUN apt-get install -y --force-yes postgresql-client > /dev/null

# Install python3
RUN apt-get install -y python3 python3-pip curl

# Install requirements
RUN pip3 install psycopg2-binary pytest
RUN pip3 install git+https://git@github.com/weecology/retriever.git

# Install Postgis after Python is setup
RUN apt-get install -y --force-yes postgis

COPY . ~/recipes
WORKDIR ~/recipes
