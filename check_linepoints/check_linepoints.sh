#!/bin/bash

set -euvo pipefail

# Extraction de linepoints

cd data 

## Extraction linepoints open data
cat opendata_routepoints.csv |xan select route_reference,stop_reference,stop_lat,stop_lon,stop_name,route_short_name |xan sort -s route_reference,stop_reference |uniq > temp_opendata_linepoints.csv

## Extraction linepoints OSM
cat osm_routepoints_for_matching.csv |xan search -s '"line_ref:FR:STIF"' "^$" -v |xan sort -s 'stop_id,"stop_ref:FR:STIF",line_id,"line_ref:FR:STIF"' |uniq |xan sort -s '"line_ref:FR:STIF"' > temp_osm_linepoints.csv

## Comptages
cd ../check_linepoints 
python3 check_linepoints.py

cd ../data
rm temp_*

