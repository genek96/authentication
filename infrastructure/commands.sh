#!/usr/bin/env bash

git clone -b master git@github.com:genek96/authentication.git --depth=1

cd authentication

docker build --no-cache -f infrastructure/Dockerfile -t innoreportsauthentication .


docker run -e FLASK_APP='/src/authentication.py' \
 -e LC_ALL='C.UTF-8' \
 -e LANG='C.UTF-8' \
 -e USER_PERSISTENCE_URL=http://10.90.138.222:5001 \
 -p 5002:5002 innoreportsauthentication:latest
