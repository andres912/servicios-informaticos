#!/bin/bash
cd /home/andy/Desktop/servicios-informaticos-staging/
git checkout staging
git pull origin
heroku git:remote -a servicios-informaticos
git push heroku main
