<div align="center">
  <h2 align="center">OSUMC Cultural Awareness App</h2>
  <p align="center">API service for the OSUMC Cultural Awareness App</p>
  <img src="https://github.com/OSUMC-Cultural-Awareness/api/workflows/Api/badge.svg" alt="Api CI"/>
  <img src="https://github.com/OSUMC-Cultural-Awareness/api/workflows/Deploy/badge.svg" alt="Deploy CI"/>
  <a href='https://coveralls.io/github/OSUMC-Cultural-Awareness/api?branch=main'><img src='https://coveralls.io/repos/github/OSUMC-Cultural-Awareness/api/badge.svg?branch=main' alt='Coverage Status' /></a>
</div>


## Getting Started

To set up a development environment follow these simple steps.

1. Clone this repo
2. If not already installed, install the following packages locally: [Docker](https://docs.docker.com/get-docker/), [python 3.8](https://www.python.org/downloads/) and [git](https://git-scm.com/downloads)
3. Create .env file with the following contents. Get secrets from another dev.
```sh
# .env
FLASK_ENV=development
FLASK_APP=__main__.py
FRONTEND_URL=http://localhost:19006/
# MONGO_URI not required for the app in dev
MONGO_URI=mongodb+srv://admin:<password>@data-cluster.tjzlp.mongodb.net/database?retryWrites=true&w=majority
MONGO_INITDB_DATABASE=database
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=<password>
MONGO_IP=172.19.199.3
MONGO_PORT=27017
# SECRET_KEY randomly generate, MUST be secure
SECRET_KEY=this-is-a-secret-key-keep-it-secret
GMAIL_ADDRESS=osumc.cultural.awareness@gmail.com
GMAIL_PASSWORD=<password>
```
4. Build docker containers. After building, api service is up and running on localhost:5000.
```sh
# build db and api containers
docker-compose up -d --build

# restore your local db from the backup file
script/restore_dev_db.sh

# if db exists, might need to drop the old db before restoring
rm -rf mongo_voume/

# all container logs
docker-compose logs -f --tail=100

# Stop containers
docker-compose down
```

- run python tests

```sh
pipenv run python -m pytest
```

## Known dev error and workaround
Immediatley after a fresh rebuild of containers it is common that the api service is not connected to mongo database and the frontend will throw an error.

Workaround: 
- add `print(db)` to `api/resource/culture.py` before line 38.
- reload the web page
- error should be gone
- remove `print(db)` from culture.py and everything will work as expected

## Deployment
`.github/workflows/deploy.yml` is automatically deploying the frontend and the backend to their respective environments. If the workflow fails, you may need to deploy manually.  
The following command will deploy the latest main branch to the ec2 instance, if you want to deploy another branch, follow these [instructions](https://github.com/OSUMC-Cultural-Awareness/docs/blob/main/setup/deployment.md#deploy-manually).

```sh
# redeploy api service
script/deploy_production_server.sh /path/to/key
```  

## Backend Production Environment
Amazon Linux 2 free-tier image running gunicorn and nginx services. Contact [@freeman91](https://github.com/freeman91) for ssh credentials.  
[Gunicorn](https://gunicorn.org/#docs) (Green Unicorn) is a Python WSGI HTTP Server for UNIX.  
Using [NginX](https://nginx.org/en/) as a HTTP and reverse proxy server, routing HTTP and HTTPS traffic to gunicorn through a socket file.  
Listening for http/s requests on www.osumc-cultural-awareness.com.  
For more information about how the AWS environment was set up refer to [this documentation](https://github.com/OSUMC-Cultural-Awareness/docs/blob/main/setup/deployment.md#aws-initial-configuration-steps)
