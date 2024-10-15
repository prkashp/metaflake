#!/bin/bash

docker build . -t metaflake/py-docker
docker run -p 8501:8501 metaflake/py-docker
