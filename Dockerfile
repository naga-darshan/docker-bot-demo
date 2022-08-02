FROM python:3.7

WORKDIR /dockerbot

COPY requirements.txt /dockerbot/requirements.txt

RUN python -m pip install -U --force pip

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /dockerbot/app

COPY README.md /dockerbot/readme.md

COPY pytest.ini /dockerbot/pytest.ini

WORKDIR /dockerbot/app

RUN apt-get update

RUN apt-get install -y vim
