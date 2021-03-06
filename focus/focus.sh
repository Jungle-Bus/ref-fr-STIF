#!/bin/bash

set -euvo pipefail

# Extraction focus

cd data 

## Extraction focus open data
xsv join route_id focus_lines.csv route_id opendata_routepoints.csv |xsv select  route_id,ZDEr_ID_REF_A,stop_lat,stop_lon,stop_name,route_short_name,dest_name |xsv sort -s route_id,dest_name,ZDEr_ID_REF_A > focus_opendata_routepoints.csv

## Extraction focus OSM
xsv join route_id focus_lines.csv osm:ref:FR:STIF:ExternalCode_Line osm_routepoints_for_matching.csv |xsv select stop_id,line_id,route_id,osm:ref:FR:STIF,osm:ref:FR:STIF:ExternalCode_Line,lat,lon,name,code,destination |xsv sort -s osm:ref:FR:STIF:ExternalCode_Line,destination,stop_id > focus_osm_routepoints.csv

