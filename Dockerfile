#!/bin/bash
FROM python:3.10


COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/logs
RUN touch /app/logs/access.log
RUN touch /app/logs/error.log

CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]