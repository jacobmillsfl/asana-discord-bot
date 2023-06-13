#!/bin/bash
# source asanaenv/bin/activate
# pip install --upgrade pip
# pip install --no-cache-dir --upgrade -r ./requirements.txt
uwsgi --ini uwsgi.ini --socket 0.0.0.0:5000 --enable-threads --protocol=http -w wsgi:app