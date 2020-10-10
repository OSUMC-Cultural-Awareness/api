#!/bin/bash

source .env
docker exec mongodb bash -c "mongorestore --archive='appdata/db-backup.bak' --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD"
