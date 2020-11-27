#!/usr/bin/env bash

# ARG $1 - private key to ssh into ec2 instance


ssh -i $1 ec2-user@18.189.142.71 OSUMC-Cultural-Awareness-App/script/restart-services.sh


