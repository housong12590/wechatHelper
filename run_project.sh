#!/usr/bin/env bash

projectName=wechat_helper

docker rmi -f ${projectName}

docker build -t ${projectName} .

docker rm -f ${projectName}

docker run -d --name ${projectName} -p 8611:5000 ${projectName}