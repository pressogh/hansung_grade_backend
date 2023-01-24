#!/bin/bash
FROM ghcr.io/multi-py/python-gunicorn-uvicorn:py3.10-LATEST

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./app app