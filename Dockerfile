FROM python:3.8-slim

RUN mkdir /appdata
WORKDIR /appdata
COPY . .

ARG FLASK_APP=$FLASK_APP
RUN pip install pipenv
RUN pipenv install

CMD [ "pipenv", "run", "flask", "run", "--host=0.0.0.0" ]
