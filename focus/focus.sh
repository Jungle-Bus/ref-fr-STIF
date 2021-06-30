#!/bin/bash

set -euvo pipefail

# Extraction focus

cd data 

## Extraction focus open data
xsv join route_id focus_lines.csv route_id opendata_routepoints.csv |xsv select ID_Line,route_id,ZDEr_ID_REF_A,stop_lat,stop_lon,stop_name,route_short_name |xsv sort -s ID_Line,ZDEr_ID_REF_A |uniq > focus_temp_opendata_linepoints.csv

## Fusion open data / OSM
xsv join ZDEr_ID_REF_A,route_id focus_temp_opendata_linepoints.csv osm:ref:FR:STIF,osm:ref:FR:STIF:ExternalCode_Line osm_routepoints_for_matching.csv |xsv select ID_Line,ZDEr_ID_REF_A,route_short_name,stop_lat,stop_lon,stop_name,name,lat,lon,stop_id,route_id[1],line_id > focus_merged.csv

rm focus_temp_opendata_linepoints.csv

