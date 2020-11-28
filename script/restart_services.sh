#!/usr/bin/env bash

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'


if [ $1 == 0 ]
  then
    echo -e "${RED}provide an ssh key as an argument${NC}"
    exit 1
fi

echo -e "${GREEN}Fetching latest master${NC}"
cd OSUMC-Cultural-Awareness-App/
git pull origin master

echo -e "${GREEN}Installing python packages${NC}"
/home/ec2-user/.local/bin/pipenv install

echo -e "${GREEN}Restarting services${NC}"
sudo systemctl daemon-reload
sudo systemctl restart gunicorn 
sudo systemctl restart nginx

echo -e "${GREEN}Production server updated${NC}"