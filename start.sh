#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

supervisord -c /src/supervisor.conf &
python /src/flask_rq.py
