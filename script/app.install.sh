#!/bin/bash

APP_DIR="./app"
# CIRCUS_FILE="/etc/circus.ini"
# CIRCUS_CONFIG="conf/circus.ini"
SETUPTOOLS="https://pypi.python.org/packages/source/s/setuptools/setuptools-3.4.4.tar.gz"
PIP="https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz"

# ----------------------
# Install virtualenv
# ----------------------
if [ ! -e venv ]; then
    #pyvenv venv # python3 (broken on Ubuntu 14.04)
    #virtualenv  # python2

    # Install on Mac OS X
    if [[ $(uname) == "Darwin" ]]; then
        # virtualenv venv  # Python2
        pyvenv venv # Python3

    # Install on Linux
    else
        # Ubuntu 14.04 is broken, recipe
        # to fix this below
        pyvenv-3.4 --without-pip venv
        source ./venv/bin/activate

        # Install setuptools
        wget $SETUPTOOLS
        tar -vzxf $(basename $SETUPTOOLS)
        cd setuptools-3.4.4
        python setup.py install
        cd ..

        # Install pip
        wget $PIP
        tar -vzxf $(basename $PIP)
        cd pip-1.5.6
        python setup.py install
        cd ..
        deactivate
    fi
fi
source ./venv/bin/activate

# Install reqs
pip install -r "$APP_DIR/requirements.txt"

deactivate


# ----------------------
# INSTALL IMG LIBS
# -------------------
if [[ $(uname) == "Darwin" ]]; then
    echo '* Skipping installing libjpeg and Co. on this Mac'
    exit
else
    # Instal libs
    sudo apt-get -y install libjpeg-dev libfreetype6-dev zlib1g-dev

    if [[ $(uname -p) == "x86_64" ]]; then
        sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
        sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
        sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

    else
        sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib
        sudo ln -s /usr/lib/i386-linux-gnu/libfreetype.so /usr/lib
        sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib
    fi
fi