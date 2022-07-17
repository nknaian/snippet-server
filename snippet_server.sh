#!/bin/bash

cd /home/pi/snippet-server
source penv/bin/activate
flask run --host=0.0.0.0
