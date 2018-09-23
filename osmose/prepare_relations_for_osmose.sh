#!/bin/bash

# Pour l'affichage dans le front Osmose, on a besoin d'associer des coordonnées
# à chaque relation

#on retire les stop_pos
xsv join stop_id osm-transit-extractor_route_stops.csv stop_point_id osm-transit-extractor_stop_points.csv |xsv select route_id,stop_id > osmose_coord_temp_route_with_stops.csv

#on garde un stop par route
cat osmose_coord_temp_route_with_stops.csv |xsv sort |xsv select stop_id,route_id|xsv fmt -t '\t'|uniq -f 1|xsv fmt -d '\t' > osmose_coord_temp_route_one_stop.csv

#on joint pour avoir la ligne de chaque route
xsv join route_id osmose_coord_temp_route_one_stop.csv route_id osm-transit-extractor_line_routes.csv |xsv select line_id,route_id,stop_id > osmose_coord_temp_line_one_stop.csv
#on joint pour avoir les coordonnées de chaque arrêt
xsv join stop_id osmose_coord_temp_line_one_stop.csv stop_point_id osm-transit-extractor_stop_points.csv |xsv select line_id,route_id,stop_id,lat,lon > osmose_relations_with_coord.csv

#on nettoie les fichiers temporaires
rm osmose_coord_temp_*
