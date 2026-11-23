#!/bin/bash

set -euvo pipefail

### Extraction des routepoints OSM

#### on retire les colonnes qu'on n'utilisera pas
cat osm_extract_lines.csv |qsv select line_id,network,ref:FR:STIF > audit_lines.csv
cat osm_extract_routes.csv |qsv select route_id,code,destination > audit_routes.csv

#### on collecte les infos des arrêts et des parcours
qsv join stop_point_id osm_extract_route_stops.csv stop_point_id osm_extract_stop_points.csv |qsv select route_id,stop_point_id,name,ref:FR:STIF,latitude,longitude > audit_stops_with_route_id.csv
qsv join route_id audit_stops_with_route_id.csv route_id audit_routes.csv |qsv select stop_point_id,name,code,destination,ref:FR:STIF,route_id,latitude,longitude > audit_stops_with_route_info.csv
echo "stop_id,name,code,destination,stop_ref:FR:STIF,route_id,latitude,longitude" > audit_stops_with_route_info_ok.csv
tail -n +2 audit_stops_with_route_info.csv >> audit_stops_with_route_info_ok.csv

#### on ajoute les infos des lignes
qsv join route_id audit_stops_with_route_info_ok.csv route_id osm_extract_line_routes.csv|qsv select stop_id,name,code,destination,stop_ref:FR:STIF,line_id,route_id,latitude,longitude > audit_stops_with_line_id.csv
qsv join line_id audit_stops_with_line_id.csv line_id audit_lines.csv |qsv sort -s stop_id |qsv sort -s network|qsv select stop_id,name,code,destination,network,stop_ref:FR:STIF,ref:FR:STIF,line_id,route_id,latitude,longitude > audit_stops_with_line_info.csv
echo "stop_id,name,code,destination,network,stop_ref:FR:STIF,line_ref:FR:STIF,line_id,route_id,latitude,longitude" > osm_routepoints.csv
tail -n +2 audit_stops_with_line_info.csv >> osm_routepoints.csv

#### on nettoie les fichiers temporaires
rm audit_*
