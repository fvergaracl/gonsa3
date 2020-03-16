#!/bin/bash
echo "*************************************"
git pull origin master
source myenv/bin/activate
pip install -r requirements.txt
kill $(lsof -i tcp:8000 | tail -n +2 | awk '{ print $2 }')
nohup python run.py & > logsgonsa3.txt 2>&1
echo "-------------------------------------"
exit 0