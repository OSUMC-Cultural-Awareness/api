#!/bin/bash

source .env
docker exec -it osumc-cultural-awareness-app_api_1 sh -c "pipenv run python -i script/db_workbench.py"
