#!/bin/bash

echo " Extraction des routepoints OSM"
echo "##### on retire les colonnes qu'on n'utilisera pas #####"
cat osm-transit-extractor_lines.csv |xsv select line_id,network,osm:ref:FR:STIF:ExternalCode_Line > audit_lines.csv
cat osm-transit-extractor_routes.csv |xsv select route_id,code,destination > audit_routes.csv

#echo "##### on retire les lignes des fichiers avec des infos manquantes #####"
#cat audit_lines.csv |xsv search -s osm:ref:FR:STIF:ExternalCode_Line '^$' -v > audit_lines_with_mapping.csv
#cat audit_routes.csv |xsv search -s destination '^$' -v|xsv search -s code '^$' -v > audit_routes_with_destination.csv
#cat osm-transit-extractor_stop_points.csv |xsv search -s osm:ref:FR:STIF '^$' -v |xsv search -s osm:public_transport platform |xsv search -s name '^$' -v > audit_stops_ok.csv

echo "##### on fusionne le tout #####"
xsv join stop_id osm-transit-extractor_route_stops.csv stop_point_id osm-transit-extractor_stop_points.csv |xsv select route_id,stop_id,name,osm:ref:FR:STIF,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,osm:wheelchair,lat,lon > audit_stops_with_route_id.csv
xsv join route_id audit_stops_with_route_id.csv route_id audit_routes.csv |xsv select stop_id,name,code,destination,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,osm:wheelchair,route_id,lat,lon > audit_stops_with_route_info.csv
xsv join route_id audit_stops_with_route_info.csv route_id osm-transit-extractor_line_routes.csv|xsv select stop_id,name,code,destination,osm:ref:FR:STIF,osm:ref:FR:STIF:stop_id,osm:wheelchair,line_id,route_id,lat,lon > audit_stops_with_line_id.csv
xsv join line_id audit_stops_with_line_id.csv line_id audit_lines.csv |xsv select stop_id,name,code,destination,network,osm:ref:FR:STIF,osm:ref:FR:STIF:ExternalCode_Line,osm:wheelchair,line_id,route_id,lat,lon,osm:ref:FR:STIF:stop_id > osm_routepoints.csv

echo "##### on nettoie les fichiers temporaires #####"
rm audit_*
