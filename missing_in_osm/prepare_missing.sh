#!/bin/bash

echo "##### on prépare les lignes opendata #####"
xsv join agency_id gtfs_routes.txt agency_id gtfs_agency.txt |xsv select agency_id,agency_name,route_id,route_short_name,route_long_name,route_type,route_color,route_text_color > opendata_lignes.csv

echo "##### on récupère l'id OSM des lignes opendata #####"
xsv join --left route_id opendata_lignes.csv osm:ref:FR:STIF:ExternalCode_Line lignes.csv|xsv select 1-8,line_id > opendata_lines_with_osm_id.csv
# /!\ on a parfois plusieurs lignes OSM pour une même ligne opendata

echo "##### on liste les lignes OSM avec un tracé #####"
cat osm-transit-extractor_lines.csv |xsv search -s shape '^$' -v |xsv select line_id > osm_lines_with_shape.csv

