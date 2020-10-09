FROM python:3.8-alpine

MAINTAINER Scott Nicholas Hackman <snickhackman@gmail.com>

RUN pip install pipenv

RUN mkdir /appdata
WORKDIR /appdata
ARG FLASK_APP=$FLASK_APP
COPY . .

RUN pipenv install

CMD [ "pipenv", "run", "flask", "run", "--host=0.0.0.0" ]
