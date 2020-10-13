import os

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

DOMAIN = os.getenv("MONGO_IP")
PORT = os.getenv("MONGO_PORT")
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE")
MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")


def connect():
    """
    establishes a connection to the database

    ENV variables:
        DOMAIN - container IP address of the mongodb container
        PORT - port expose on the mongodb container
        MONGO_INITDB_DATABASE - database name
        MONGO_INITDB_ROOT_USERNAME - root access username
        MONGO_INITDB_ROOT_PASSWORD - root access user password

    Returns:
        a database instance with name MONGO_INITDB_DATABASE

    Raises:
        a ServerSelectionTimeoutError when connection takes more than 3 seconds
    """
    try:
        # try to instantiate a client instance
        client = MongoClient(
            host=[DOMAIN + ":" + PORT],
            serverSelectionTimeoutMS=5000,  # 3 second timeout
            username=MONGO_INITDB_ROOT_USERNAME,
            password=MONGO_INITDB_ROOT_PASSWORD,
        )

        # print the version of MongoDB server if connection successful
        print("server version:", client.server_info()["version"])

        return client[MONGO_INITDB_DATABASE]

    except ServerSelectionTimeoutError as err:
        client = None

        # catch pymongo.errors.ServerSelectionTimeoutError
        print("pymongo ERROR:", err)
