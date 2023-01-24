#!/bin/bash
FROM python:3.10

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

WORKDIR /app

RUN mkdir /app/logs
RUN touch /app/logs/access.log
RUN touch /app/logs/error.log

CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]