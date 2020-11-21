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
  <img src="https://coveralls.io/repos/github/freeman91/OSUMC-Cultural-Awareness-App/badge.svg?branch=master" alt="Api Coverage"/>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Configuration](#Installation-&-Configuration)
  - [Usage](#Usage)
- [Contributors](#contributors)

<!-- ABOUT THE PROJECT -->

## About The Project

TODO

### Built With

MongoDB
Python-Flask
Node
React-Native

<!-- GETTING STARTED -->

## Getting Started

To set up a development environment follow these simple steps.

### Prerequisites

install the following packages

- [Docker](https://docs.docker.com/get-docker/)
- [python 3.8](https://www.python.org/downloads/)
- [node](https://nodejs.org/en/download/)
- [expo-cli](https://docs.expo.io/get-started/installation/)

### Installation & Configuration

1. Clone the repo

```sh
git clone https://github.com/freeman91/OSUMC-Cultural-Awareness-App.git
```

2. Create .env file with the following contents. Get secrets from another dev.

```sh
FLASK_ENV=development
FLASK_APP=api/__main__.py
MONGO_URI=mongodb://localhost:27017/
MONGO_INITDB_DATABASE=database
MONGO_INITDB_ROOT_USERNAME=user
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_IP=172.19.199.3
MONGO_PORT=27017

# SECRET_KEY randomly generate, MUST be secure
SECRET_KEY=this-is-a-secret-key-keep-it-secret

GMAIL_ADDRESS=osumc.cultural.awareness@gmail.com
GMAIL_PASSWORD=password
```

3. Install NPM packages

```sh
yarn install
# or
npm install
```

<!-- USAGE EXAMPLES -->

### Usage

```sh
# build db and api containers
docker-compose up -d --build

# restore your local db from the backup file
script/restore_dev_db.sh

# start expo service [android simulator, ios simulator, web browser]
expo start [-a, -i, -w]
```

testing

```sh
pipenv shell

python -m pytest
```

```sh
# all container logs
docker-compose logs -f --tail=100

# Stop containers
docker-compose down
```

<!-- Contributers -->

## Contributors

- Addison Freeman
- Nick Lamanna
- Adam Claus
- Nick Hackman

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- [Rajiv Ramnath]()
- [Roy Dunfee]()
