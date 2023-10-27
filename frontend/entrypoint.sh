#!/bin/bash

# If command is entered, run it. Otherwise, run server
if [ "$#" != "0" ]; then
    exec "$@"
else
    # Install requirements
    yarn install
    exec yarn start
fi
