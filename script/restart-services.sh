#!/usr/bin/env bash


cd OSUMC-Cultural-Awareness-App/
git fetch

# change to master
git pull origin deploy-script

~/.local/bin/pipenv install

sudo systemctl daemon-reload

sudo systemctl restart gunicorn 

sudo systemctl restart nginx