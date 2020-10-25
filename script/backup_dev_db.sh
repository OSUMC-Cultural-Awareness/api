#!/usr/bin/env bash

source .env
docker exec mongodb bash -c "mongodump --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --archive='appdata/db-backup.bak'"
