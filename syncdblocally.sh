#!/bin/bash
heroku pgbackups:capture --expire
curl -o latest.dump `heroku pgbackups:url`
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U memestat -d memestat_db latest.dump
