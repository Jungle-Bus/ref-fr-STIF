#!/bin/bash

set -euvo pipefail

# Mise à jour de la liste des parcours pour MicrocOSM
cd data 
cat osm_extract_routes.csv |xan search -s mode '(bus|coach)' |xan select 'route_id,name,code,destination,network' > idf_routes.csv