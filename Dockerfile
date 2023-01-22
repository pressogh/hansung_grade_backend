#!/bin/bash
FROM ghcr.io/multi-py/python-gunicorn-uvicorn:py3.10-LATEST

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app