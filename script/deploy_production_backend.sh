#!/usr/bin/env bash

ssh -i $1 ec2-user@18.189.142.71 api/script/restart_services.sh
