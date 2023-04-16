#!/bin/bash

# install dependencies
apt-get update
apt-get install ffmpeg libsm6 libxext6  -y
apt-get install -y python3 python3-pip
pip3 install -r requirements.txt

# run dev server (probs enough)
cd ./app
export STORE_SECRET=$1
python3 manage.py runserver 0.0.0.0:80
