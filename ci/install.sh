#!/bin/bash

set -ev

# install python dependencies for Osmose
pip3 install xmltodict

# install prism
git clone --branch=add_tags https://github.com/Jungle-Bus/prism
cd prism
poetry install