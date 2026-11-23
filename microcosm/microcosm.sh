#!/bin/bash

set -euvo pipefail

# Mise à jour de la liste des parcours pour MicrocOSM
cd data 
cat osm_extract_routes.csv |qsv search -s mode '(bus|coach)' |qsv select 'route_id,name,code,destination,network' > idf_routes.csv