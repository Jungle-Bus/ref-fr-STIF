#!/bin/bash

set -ev

# install osm-transit-extractor
wget https://github.com/CanalTP/osm-transit-extractor/releases/download/v0.3.0/osm_transit_extractor_v0.3.0-x86_64-linux.zip
unzip osm_transit_extractor_v0.3.0-x86_64-linux.zip

# install xsv
wget https://github.com/BurntSushi/xsv/releases/download/0.13.0/xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz
tar -zxvf xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz

# install python dependencies
pip3 install xmltodict
