# Scripts guide

## Dependencies

- docker containers up and running `docker-compose up -d --build`
- .env file with MONGO env vars

## Script Descriptions

- `backup_dev_db.sh`  
  run `script/backup_dev_db.sh` to create a backup (`db-backup.bak`) of the database running in the mongo docker container

- `restore_dev_db.sh`  
  run `script/restore_dev_db.sh` to restore the database running in the mongo container with a backup (`db-backup.bak`)

- `pyshell_db.sh`  
  run `script/pyshell_db.sh` to open a python shell and load `db_workbench.py`.  
  use the db instance to run any pymongo db operation or you can call the functions from `db_workbench.py` that are common db operations

- `db_workbench.py`  
  loaded by `pyshell_db.sh`.  
  Exposes an instance of the database and contains functions for common db operations
