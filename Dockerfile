FROM python:3.7-bullseye
COPY . /clara-api-server
WORKDIR /clara-api-server
RUN mkdir -p submissions clusters
CMD . /clara-api-server/dockerscript.sh