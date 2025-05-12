#!/bin/bash

git pull

docker stop bot

docker rm bot

docker build -t bot .

docker run -d \
  --name bot \
  --restart unless-stopped \
  --env-file .env \
  bot
