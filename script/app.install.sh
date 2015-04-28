#!/bin/bash

APP_DIR="./app"
# CIRCUS_FILE="/etc/circus.ini"
# CIRCUS_CONFIG="conf/circus.ini"


# ----------------------
# Install virtualenv
# ----------------------
if [ ! -e venv ]; then
    pyvenv venv # python3
    #virtualenv  # python2
fi
source venv/bin/activate

# Install reqs
pip install -r "$APP_DIR/requirements.txt"

deactivate


# ----------------------
# Other
# ----------------------
