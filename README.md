<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="./public/osu-cse-logo.jpg" alt="Logo" width="580" height="80">

  <h3 align="center">OSUMC Cultural Awareness App</h3>

  <p align="center">
    This app is intended for health care professionals, to aid in their understanding of the cultural norms of their patients
  </p>
  <img src="https://github.com/freeman91/OSUMC-Cultural-Awareness-App/workflows/Frontend/badge.svg" alt="Frontend CI"/>
  <img src="https://github.com/freeman91/OSUMC-Cultural-Awareness-App/workflows/Api/badge.svg" alt="Api CI"/>
  <img src="https://github.com/freeman91/OSUMC-Cultural-Awareness-App/workflows/Deploy/badge.svg" alt="Api CI"/>
  <a href="https://coveralls.io/github/freeman91/OSUMC-Cultural-Awareness-App?branch=master"><img src="https://coveralls.io/repos/github/freeman91/OSUMC-Cultural-Awareness-App/badge.svg?branch=master" alt="Api Coverage"/> </a>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Tech Stack](#tech-stack)
  - [Backend Production Environment](#backend-production-environment)
  - [Frontend Production Environment](#frontend-production-environment)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Configuration](#Installation-&-Configuration)
    - [Build Backend Containers](#build-backend-containers)
- [Deployment](#deployment)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Contributors](#contributors)
- [Acknowledgements](#acknowledgements)

***

## About The Project
### Tech Stack

- MongoDB  
- Python-Flask  
- Node  
- React-Native  


### Backend Production Environment
Amazon Linux 2 free-tier image running gunicorn and nginx services. Contact @freeman91 for ssh credentials.  
[Gunicorn](https://gunicorn.org/#docs) (Green Unicorn) is a Python WSGI HTTP Server for UNIX.  
Using [NginX](https://nginx.org/en/) as a HTTP and reverse proxy server, routing HTTP and HTTPS traffic to gunicorn through a socket file.  
Listening for http/s requests on www.osumc-cultural-awareness.com.  

### Frontend Production Environment
Utlizing [Github Pages](https://pages.github.com/) to deploy a web build of the React Native application.  
[Live React Native App](https://freeman91.github.io/OSUMC-Cultural-Awareness-App/)

***

## Getting Started

To set up a development environment follow these simple steps.

### Prerequisites

install the following packages

- [Docker](https://docs.docker.com/get-docker/)
- [python 3.8](https://www.python.org/downloads/)
- [node](https://nodejs.org/en/download/)
- [expo-cli](https://docs.expo.io/get-started/installation/)
- [mongo](https://www.mongodb.com/try/download/community)(optional)

### Installation & Configuration for a dev environment

1. Clone this repo
2. In app root, create .env file with the following contents. Get secrets from another dev.

```sh
FLASK_ENV=development
FLASK_APP=api/__main__.py
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

3. Install yarn packages

```sh
yarn install
```

4. Build backend docker containers

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

After building, api service is up and running on localhost:5000.

5. Start Expo, React Native service 
```sh
yarn start
```

- run python tests

```sh
pipenv shell
python -m pytest
```

***

## Deployment
`.github/workflows/deploy.yml` is automatically deploying the frontend and the backend to their respective environments. If either of those fail, you may need to deploy manually.

### Backend
This will deploy the latest master, if you want to deploy another branch, follow these [instructions](https://github.com/freeman91/OSUMC-Cultural-Awareness-App/blob/master/docs/deployment.md#deploy-manually).

```sh
script/deploy_production_server.sh /path/to/key
```  

### Frontend 
```sh
yarn deploy
```

***

## Contributors

- Addison Freeman, @freeman91
- Nick Lamanna
- Adam Claus
- Nick Hackman

## Acknowledgements

- [Rajiv Ramnath]()
- [Roy Dunfee]()
