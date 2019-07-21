FROM python:3.7
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH /innerio/api

RUN mkdir /innerio
WORKDIR /innerio

COPY requirements.txt /innerio/
COPY innerio.json /innerio/

RUN pip3 install -r requirements.txt
COPY . /innerio/