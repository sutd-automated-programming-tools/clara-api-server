from python:3.7-bullseye
COPY . /clara-api-server
WORKDIR /clara-api-server
RUN mkdir submissions clusters
CMD . /clara-api-server/dockerscript.sh