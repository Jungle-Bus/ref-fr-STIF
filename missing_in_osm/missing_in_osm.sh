#!/bin/bash

set -euvo pipefail

# État des lieux par réseau des lignes OSM à créer ou au tracé manquant

cd data

## préparation des lignes open data
xsv join agency_id gtfs_routes.txt agency_id gtfs_agency.txt |xsv select agency_id,agency_name,route_id,route_short_name,route_long_name,route_type,route_color,route_text_color |xsv sort -s route_id|xsv sort -s agency_name > opendata_lignes.csv
sed -i -e "s/IDFM://g" opendata_lignes.csv


## ajout de l'id OSM sur les lignes open data
xsv join --left route_id opendata_lignes.csv osm:ref:FR:STIF lignes.csv|xsv select 1-8,line_id > opendata_lines_with_osm_id.csv
# /!\ on a parfois plusieurs lignes OSM pour une même ligne opendata

## extraction des lignes OSM avec un tracé déjà existant
cat osm-transit-extractor_lines.csv |xsv search -s shape '^$' -v |xsv select line_id > osm_lines_with_shape.csv

## analyse des lignes opendata
cd ../missing_in_osm && python3 missing_lines.py > ../data/missing.md
