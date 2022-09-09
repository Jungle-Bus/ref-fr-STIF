#!/bin/bash

set -euvo pipefail

# Mise à jour des analyses Osmose

cd data

## extraction de coordonnées pour les relations OSM

#### on retire les stop_pos
xsv join stop_id osm-transit-extractor_route_points.csv stop_point_id osm-transit-extractor_stop_points.csv |xsv select route_id,stop_id > osmose_coord_temp_route_with_stops.csv

#### on garde un stop par route
cat osmose_coord_temp_route_with_stops.csv |xsv sort |xsv select stop_id,route_id|xsv fmt -t '\t'|uniq -f 1|xsv fmt -d '\t' > osmose_coord_temp_route_one_stop.csv

#### on joint pour avoir la ligne de chaque route
xsv join route_id osmose_coord_temp_route_one_stop.csv route_id osm-transit-extractor_line_routes.csv |xsv select line_id,route_id,stop_id > osmose_coord_temp_line_one_stop.csv

#### on joint pour avoir les coordonnées de chaque arrêt
xsv join stop_id osmose_coord_temp_line_one_stop.csv stop_point_id osm-transit-extractor_stop_points.csv |xsv select line_id,route_id,stop_id,lat,lon > osmose_relations_with_coord.csv

#### on nettoie les fichiers temporaires
rm osmose_coord_temp_*

## création des erreurs Osmose
cd ../osmose 
python3 create_osmose_xml.py

## préparation de l'envoi
cd ../data
bzip2 osmose_*

## envoi des erreurs sur les lignes
curl -s --request POST --form analyser='opendata_stif' --form country='france_ile_de_france' --form code=\"$Osmose_idf_auth\" --form content=@osmose_lines.xml.bz2 https://osmose.openstreetmap.fr/control/send-update

## envoi des erreurs sur les arrêts
curl -s --request POST --form analyser='opendata_stif' --form country='france_ile_de_france' --form code=\"$Osmose_idf_auth\" --form content=@osmose_stops.xml.bz2 https://osmose.openstreetmap.fr/control/send-update
