#!/bin/bash

echo " Extraction des routepoints GTFS"
echo "##### on calcule des trip points #####"
xsv join trip_id gtfs_trips.txt trip_id gtfs_audit_stoptime_lite.csv  |xsv select 'route_id,stop_id,direction_id,trip_id' > gtfs_audit_trippoints.csv

echo "##### on ajoute les destinations et on filtre les duplicats #####"
xsv join trip_id gtfs_audit_trippoints.csv trip_id gtfs_audit_trip_destinations.csv |xsv select 'route_id,stop_id,direction_id,trip_dest_id' |xsv sort |uniq > gtfs_audit_routepoints_1.csv

echo "##### on ajoute les infos de l'arrêt #####"
xsv join stop_id gtfs_audit_routepoints_1.csv stop_id gtfs_stop_extensions.txt |xsv select '!stop_id[1]' > gtfs_audit_routepoints_2.csv
xsv join stop_id gtfs_audit_routepoints_2.csv stop_id gtfs_stops.txt |xsv select 'stop_id,route_id,ZDEr_ID_REF_A,stop_name,stop_lat,stop_lon,wheelchair_boarding,trip_dest_id' > gtfs_audit_routepoints_3.csv

echo "##### on ajoute le nom de l'arrêt de destination #####"
xsv join trip_dest_id gtfs_audit_routepoints_3.csv stop_id gtfs_stops.txt |xsv select 'stop_id[0],route_id,ZDEr_ID_REF_A,stop_name[0],stop_lat[0],stop_lon[0],wheelchair_boarding,stop_name[1]' > gtfs_audit_routepoints_4.csv

echo "##### on renomme pour éviter les doublons de colonnes #####"
echo "stop_id,route_id,ZDEr_ID_REF_A,stop_name,stop_lat,stop_lon,wheelchair_boarding,dest_name" > gtfs_audit_gtfs_routepoints.csv
tail -n +2 gtfs_audit_routepoints_4.csv >> gtfs_audit_gtfs_routepoints.csv

echo "##### on affiche les informations sur la ligne #####"
xsv join route_id gtfs_audit_gtfs_routepoints.csv route_id gtfs_routes.txt | xsv select stop_id,route_id,ZDEr_ID_REF_A,stop_name,stop_lat,stop_lon,wheelchair_boarding,dest_name,route_short_name,agency_id > gtfs_audit_routepoints_with_code.csv
xsv join agency_id gtfs_audit_routepoints_with_code.csv agency_id gtfs_agency.txt | xsv select stop_id,route_id,ZDEr_ID_REF_A,stop_name,stop_lat,stop_lon,wheelchair_boarding,dest_name,route_short_name,agency_name > gtfs_routepoints.csv

echo "##### on nettoie, on n'est pas des porcs ;) #####"
rm gtfs_audit_*
