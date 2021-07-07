#!/bin/bash

set -euvo pipefail

### Extraction des routepoints GTFS

#### on simplifie le fichier stop_times
cat gtfs_stop_times.txt |xsv select trip_id,stop_id,stop_sequence |xsv search -s stop_id StopPlace -v > gtfs_audit_stoptime_lite.csv

#### on calcule des trip points
xsv join trip_id gtfs_trips.txt trip_id gtfs_audit_stoptime_lite.csv  |xsv select 'route_id,wheelchair_accessible,stop_id,direction_id,trip_id,trip_headsign' > gtfs_audit_trippoints.csv

#### on ajoute les destinations et on filtre les duplicats
cat gtfs_audit_trippoints.csv |xsv select 'route_id,wheelchair_accessible,stop_id,direction_id,trip_headsign' |xsv sort |uniq > gtfs_audit_routepoints_1.csv

#### on ajoute les infos de l'arrêt
xsv join stop_id gtfs_audit_routepoints_1.csv stop_id gtfs_stops.txt |xsv select 'stop_id,route_id,wheelchair_accessible,stop_name,stop_lat,stop_lon,wheelchair_boarding,trip_headsign' > gtfs_audit_routepoints_3.csv

#### on renomme pour éviter les doublons de colonnes
echo "stop_reference,route_reference,route_wheelchair,stop_name,stop_lat,stop_lon,stop_wheelchair,dest_name" > gtfs_audit_gtfs_routepoints.csv
tail -n +2 gtfs_audit_routepoints_3.csv >> gtfs_audit_gtfs_routepoints.csv

#### on affiche les informations sur la ligne
xsv join route_reference gtfs_audit_gtfs_routepoints.csv route_id gtfs_routes.txt | xsv select stop_reference,route_reference,route_wheelchair,stop_name,stop_lat,stop_lon,stop_wheelchair,dest_name,route_short_name,agency_id,route_type |xsv search -s route_type 3 |xsv select '!route_type' > gtfs_audit_routepoints_with_code.csv
xsv join agency_id gtfs_audit_routepoints_with_code.csv agency_id gtfs_agency.txt | xsv sort -s route_reference,dest_name,stop_reference | xsv select stop_reference,route_reference,route_wheelchair,stop_name,stop_lat,stop_lon,stop_wheelchair,dest_name,route_short_name,agency_name > opendata_routepoints.csv

#### on retire le préfixe
sed -i -e "s/IDFM://g" opendata_routepoints.csv

#### on nettoie les fichiers temporaires
rm gtfs_audit_*

