#!/usr/bin/env bash

source .env
docker exec -it api_flask_1 sh -c "pipenv run python -i script/db_workbench.py"
