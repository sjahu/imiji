#!/bin/bash

export FLASK_APP=src/imiji
export FLASK_ENV=development # disable in production
export PYTHONPATH=${PYTHONPATH}:$(pwd)/imiji # add to path so __init__ can find other files
flask run
