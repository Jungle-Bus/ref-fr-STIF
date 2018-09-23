#!/bin/bash

set -ev

# install factotum
wget https://bintray.com/artifact/download/snowplow/snowplow-generic/factotum_0.5.0_linux_x86_64.zip
unzip factotum_0.5.0_linux_x86_64.zip

# install osm-transit-extractor
wget https://github.com/CanalTP/osm-transit-extractor/releases/download/v0.1.0/osm_transit_extractor_v0.1.0-x86_64-linux.zip
unzip osm_transit_extractor_v0.1.0-x86_64-linux.zip

# install xsv
wget https://github.com/BurntSushi/xsv/releases/download/0.13.0/xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz
tar -zxvf xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz

# install python dependencies
pip3 install xmltodict
