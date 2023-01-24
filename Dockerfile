#!/bin/bash
FROM python:3.10

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

# make gunicorn.socket file at /etc/systemd/system
RUN touch /etc/systemd/system/gunicorn.socket
RUN echo "[Unit]" >> /etc/systemd/system/gunicorn.socket
RUN echo "Description=gunicorn socket" >> /etc/systemd/system/gunicorn.socket
RUN echo "" >> /etc/systemd/system/gunicorn.socket
RUN echo "[Socket]" >> /etc/systemd/system/gunicorn.socket
RUN echo "ListenStream=/run/gunicorn.sock" >> /etc/systemd/system/gunicorn.socket
RUN echo "" >> /etc/systemd/system/gunicorn.socket
RUN echo "[Install]" >> /etc/systemd/system/gunicorn.socket
RUN echo "WantedBy=sockets.target" >> /etc/systemd/system/gunicorn.socket

# make gunicorn.service file at /etc/systemd/system
RUN touch /etc/systemd/system/gunicorn.service
RUN echo "[Unit]" >> /etc/systemd/system/gunicorn.service
RUN echo "Description=gunicorn daemon" >> /etc/systemd/system/gunicorn.service
RUN echo "Requires=gunicorn.socket" >> /etc/systemd/system/gunicorn.service
RUN echo "After=network.target" >> /etc/systemd/system/gunicorn.service
RUN echo "" >> /etc/systemd/system/gunicorn.service
RUN echo "[Service]" >> /etc/systemd/system/gunicorn.service
RUN echo "User=hansung-grade-backend" >> /etc/systemd/system/gunicorn.service
RUN echo "Group=www-data" >> /etc/systemd/system/gunicorn.service
RUN echo "WorkingDirectory=/app" >> /etc/systemd/system/gunicorn.service
RUN echo "ExecStart=gunicorn -c /app/gunicorn_conf.py main:app" >> /etc/systemd/system/gunicorn.service

CMD ["systemctl", "start", "gunicorn.socket"]
CMD ["systemctl", "enable", "gunicorn.socket"]