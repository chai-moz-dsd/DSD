#!/usr/bin/env bash

export IMAGE_JENKINS=ubuntu/jenkins
export JENKINS_HOME=/var/jenkins_home
export CONTAINER_JENKINS_SERVER=jenkins-server
export CONTAINER_REGISTRY_SERVER=registry-server

docker build -t ${IMAGE_JENKINS} .

# Start jenkins server
docker ps -a | grep ${CONTAINER_JENKINS_SERVER} | awk '{print $1}' | xargs --no-run-if-empty docker rm -f

docker run -d --name ${CONTAINER_JENKINS_SERVER} \
 --restart=always \
 -p 8080:8080 \
 -v /var/run/docker.sock:/var/run/docker.sock:ro \
 -v /usr/local/bin/docker-compose:/usr/local/bin/docker-compose:ro \
 -v $HOME/.ssh/primero-aws.pem:/root/.ssh/primero-aws.pem \
 -v ${JENKINS_HOME}:${JENKINS_HOME} \
 ${IMAGE_JENKINS}


# Start registry server

docker ps -a | grep ${CONTAINER_REGISTRY_SERVER} | awk '{print $1}' | xargs --no-run-if-empty docker rm -f

docker run -d --name ${CONTAINER_REGISTRY_SERVER} \
 --restart=always \
 -e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/data \
 -v $HOME/.registry_home:/data \
 -p 5000:5000 \
 registry:2
