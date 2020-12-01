# Scripts guide

## Dependencies

- docker containers up and running `docker-compose up -d --build`
- .env file with MONGO env vars

## Script Descriptions

- `backup_prod_db.sh`  
  run `script/backup_prod_db.sh` to create a backup (`db-backup.bak`) of the mongo atlas cloud cluster

- `restore_dev_db.sh`  
  run `script/restore_dev_db.sh` to restore the database running in the mongo container with a backup (`db-backup.bak`)

- `pyshell_db.sh`  
  run `script/pyshell_db.sh` to open a python shell and load `db_workbench.py`.  
  use the db instance to run any pymongo db operation or you can call the functions from `db_workbench.py` that are common db operations

- `db_workbench.py`  
  loaded by `pyshell_db.sh`.  
  Exposes an instance of the database and contains functions for common db operations

- `deploy_production_backend.sh`
  Manually deploy latest main branch to production the server
  Executes `restart_services.sh` inside of the ec2 instance
  Must pass this script ssh key for the server

- `restart_services.sh`
  Should only run on the backend production server
  Pulls latest main branch, updates python dependencies, restarts gunicorn, nginx services
  