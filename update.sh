#!/bin/bash
echo 'START UPDATE.........................'


echo 'PULL CODE.........................'
pwd
sudo git pull


echo 'RELOAD SERVER.........................'
docker exec -td fastapi_example sh start-reload.sh

echo 'END UPDATE.........................'

echo 'RESTART FastAPI.........................'
# docker-compose restart
