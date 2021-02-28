#!/bin/bash

set -euvo pipefail

# Mise à jour de la liste des parcours pour MicrocOSM
cd data 
cat osm-transit-extractor_routes.csv |xsv search -s mode '(bus|coach)' |xsv select '1-4,8' > idf_routes.csv