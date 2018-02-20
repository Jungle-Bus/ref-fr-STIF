# Audit comparatif OSM / STIF

WIP

Afin de gommer les divergences de modélisation, on extrait des routepoints,
c'est-à-dire un object fictif qui représente un arrêt desservi par une ligne dans une direction.
Si deux lignes s'arrêtent à un arrêt, il est représenté par deux routepoints.

Schéma attendu pour les routepoints :
* un id
* un code de ligne (de parcours en fait)
* terminus de ligne (de parcours en fait)
* code STIF de la ligne
* code STIF de l'arrêt
* nom de l'arrêt
* éventuellement des infos complémentaires sur l'arrêt


cat gtfs_stop_times.txt |xsv select trip_id,stop_id,stop_sequence > gtfs_audit_stoptime_lite.csv

python gtfs_add_terminus_to_trips.py

xsv join trip_id gtfs_audit_stoptime_lite.csv trip_id gtfs_trips.txt |xsv select 'route_id,stop_id,direction_id,trip_id' > gtfs_audit_trippoints.csv

xsv join trip_id gtfs_audit_trippoints.csv trip_id gtfs_audit_trip_destinations.csv |xsv select 'route_id,stop_id,direction_id,trip_dest_id' |xsv sort |uniq > gtfs_audit_routepoints_1.csv

xsv join stop_id gtfs_audit_routepoints_1.csv stop_id gtfs_stop_extensions.txt |xsv select '!stop_id[1]' > gtfs_audit_routepoints_2.csv

xsv join stop_id gtfs_audit_routepoints_2.csv stop_id gtfs_stops.txt |xsv select 'stop_id,route_id,ZDEr_ID_REF_A,stop_name,stop_lat,stop_lon,wheelchair_boarding,trip_dest_id' > gtfs_audit_routepoints_3.csv

xsv join trip_dest_id gtfs_audit_routepoints_3.csv stop_id gtfs_stops.txt |xsv select 'stop_id[0],route_id,ZDEr_ID_REF_A,stop_name[0],stop_lat[0],stop_lon[0],wheelchair_boarding,stop_name[1]' > gtfs_audit_routepoints_4.csv

echo "stop_id,route_id,ZDEr_ID_REF_A,stop_name,stop_lat,stop_lon,wheelchair_boarding,dest_name" > gtfs_routepoints.csv
tail -n +2 gtfs_audit_routepoints_4.csv >> gtfs_routepoints.csv 