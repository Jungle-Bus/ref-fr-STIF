#!/bin/bash

set -euvo pipefail

# Extraction de routepoints pour OSM et l'open data

cd data

## Extraction des routepoints du GTFS

../audit_routepoints/prepare_gtfs_routepoints.sh

## Extraction des routepoints d'OSM

../audit_routepoints/prepare_osm_routepoints.sh

## duplication des routepoints OSM avec plusieurs ref STIF
cd ../audit_routepoints 
python3 osm_duplicate_if_has_multiple_ref.py