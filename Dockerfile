FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Time
ENV TZ "Asia/Shanghai"
ENV TERM xtermENV TERM xterm

# PIP Mirror
RUN mkdir -p /root/.pip/
ADD deploy/pip.conf /root/.pip/

# Project dir
RUN rm -rf /app/ && mkdir -p /app/
COPY ./ /app
WORKDIR /app/

# Log dir
RUN mkdir -p /app/logs/

# Requirements install
RUN pip install --no-cache-dir -r requirements.txt


