#!/usr/bin/env bash

source .env
mongodump --uri="mongodb+srv://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@data-cluster.tjzlp.mongodb.net" --archive='db-backup.bak'
