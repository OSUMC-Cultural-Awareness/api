#!/usr/bin/env bash

# TODO
# error checking on each command
# how to pass ssh key to github actions

set -e

GREEN='\033[0;31m'
RED='\033[0;31m'
NC='\033[0m'


if [ $1 == 0 ]
  then
    echo "${RED}provide an ssh key as an argument${NC}"
    exit 1
fi

echo "${GREEN}Fetching latest master${NC}"
cd OSUMC-Cultural-Awareness-App/
git fetch
# change to master
git pull origin deploy-script

echo "${GREEN}Installing python packages${NC}"
/home/ec2-user/.local/bin/pipenv install

echo "${GREEN}Restarting services${NC}"
sudo systemctl daemon-reload
sudo systemctl restart gunicorn 
sudo systemctl restart nginx
