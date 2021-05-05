#!/bin/bash
cd ..
docker build --no-cache -t cicd:display-generator .
docker tag cicd:display-generator registry:5000/display-generator:$VERSION
docker push registry:5000/display-generator:$VERSION
docker rmi cicd:display-generator


