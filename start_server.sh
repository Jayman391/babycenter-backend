#!/bin/bash

#activate the virtual environment
source venv/bin/activate
# install pdm
pip install pdm
# install deps
pdm install
# Run the app using Gunicorn
pdm run gunicorn -w 4 -b 0.0.0.0:8000 server:app
