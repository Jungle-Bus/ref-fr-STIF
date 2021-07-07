#!/bin/bash

set -euvo pipefail

# Extraction focus

cd data 

## Extraction focus open data
xsv join ID_Line focus_lines.csv route_reference opendata_routepoints.csv |xsv select route_reference,stop_reference,stop_lat,stop_lon,stop_name,route_short_name |xsv sort -s route_reference,stop_reference |uniq > focus_temp_opendata_linepoints.csv

## Fusion open data / OSM
xsv join stop_reference,route_reference focus_temp_opendata_linepoints.csv stop_ref:FR:STIF,line_ref:FR:STIF osm_routepoints_for_matching.csv |xsv select route_reference,stop_reference,route_short_name,stop_lat,stop_lon,stop_name,name,lat,lon,stop_id,route_id,line_id > focus_merged.csv

rm focus_temp_opendata_linepoints.csv

