#!/bin/bash

set -euvo pipefail

### Extraction des routepoints OSM

#### on retire les colonnes qu'on n'utilisera pas
cat osm-transit-extractor_lines.csv |xsv select line_id,network,osm:ref:FR:STIF:ExternalCode_Line,osm:wheelchair > audit_lines.csv
cat osm-transit-extractor_routes.csv |xsv select route_id,code,destination,osm:wheelchair > audit_routes.csv

#### on collecte les infos des arrêts et des parcours
xsv join stop_id osm-transit-extractor_route_points.csv stop_point_id osm-transit-extractor_stop_points.csv |xsv select route_id,stop_id,name,osm:ref:FR:STIF,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,osm:wheelchair,lat,lon > audit_stops_with_route_id.csv
xsv join route_id audit_stops_with_route_id.csv route_id audit_routes.csv |xsv select stop_id,name,code,destination,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,osm:wheelchair[0],osm:wheelchair[1],route_id,lat,lon > audit_stops_with_route_info.csv
echo "stop_id,name,code,destination,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,stop_wheelchair,route_wheelchair,route_id,lat,lon" > audit_stops_with_route_info_ok.csv
tail -n +2 audit_stops_with_route_info.csv >> audit_stops_with_route_info_ok.csv

#### on ajoute les infos des lignes
xsv join route_id audit_stops_with_route_info_ok.csv route_id osm-transit-extractor_line_routes.csv|xsv select stop_id,name,code,destination,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,stop_wheelchair,route_wheelchair,line_id,route_id,lat,lon > audit_stops_with_line_id.csv
xsv join line_id audit_stops_with_line_id.csv line_id audit_lines.csv |xsv sort -s stop_id |xsv sort -s network|xsv select stop_id,name,code,destination,network,osm:ref:FR:STIF,osm:ref:FR:STIF:ExternalCode_Line,stop_wheelchair,route_wheelchair,osm:wheelchair,line_id,route_id,lat,lon,osm:ref:FR:STIF:stop_id > audit_stops_with_line_info.csv
echo "stop_id,name,code,destination,network,osm:ref:FR:STIF,osm:ref:FR:STIF:ExternalCode_Line,stop_wheelchair,route_wheelchair,line_wheelchair,line_id,route_id,lat,lon,osm:ref:FR:STIF:stop_id" > osm_routepoints.csv
tail -n +2 audit_stops_with_line_info.csv >> osm_routepoints.csv

#### on nettoie les fichiers temporaires
rm audit_*
