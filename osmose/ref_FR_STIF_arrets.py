#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def generate_osmose_errors_for_stops():
    errors = []
    ref_STIF_list = []
    with open('../data/gtfs_stops.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader :
            open_data_ref = row['stop_id'].replace("IDFM:", "")
            # lot of garbage here actually (stop_area, access, monomodalSP, etc)
            # maybe use opendata_routepoints file or
            # another file from IDFM open data platform instead ?
            ref_STIF_list.append(open_data_ref)

    with open('../data/osm-transit-extractor_stop_points.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            error = {"id" : row['stop_point_id'].split(':')[-1] }
            if not row['osm:ref:FR:STIF']:
                continue
            osm_ref = row['osm:ref:FR:STIF']
            if ';' in osm_ref :
                has_at_least_one_wrong_ref = False
                for a_ref in osm_ref.split(';'):
                    if a_ref.strip() not in ref_STIF_list :
                        has_at_least_one_wrong_ref = True
                if has_at_least_one_wrong_ref:
                    error['label'] = "Une des valeurs de ref:FR:STIF n'existe pas ou plus."
                    error['label'] += " Voir sur https://ref-lignes-stif.5apps.com/stop.html?osm_stop_id={}".format(error['id'])
                    error['lat'], error['lon'] = row['lat'], row['lon']
                    errors.append(error)
                continue

            try :
                int(osm_ref)
            except ValueError :
                error['label'] = "la ref:FR:STIF '{}' n'est pas numérique".format(osm_ref)
                error['lat'], error['lon'] = row['lat'], row['lon']
                errors.append(error)
                continue

            if osm_ref not in ref_STIF_list :
                error['label'] = "La ref:FR:STIF {} n'existe pas ou plus".format(osm_ref)
                error['lat'], error['lon'] = row['lat'], row['lon']
                errors.append(error)

    return errors

def generate_osmose_errors_for_routepoints():
    errors = []
    all_ref_STIF = {}
    all_lines_ref_STIF = set()
    with open('../data/opendata_routepoints.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader :
            all_ref_STIF.setdefault(row["stop_reference"],set()).add(row["route_reference"])
            all_lines_ref_STIF.add(row["route_reference"])

    ref_STIF_list = all_ref_STIF.keys()

    osm_dedup_id_list = []
    with open('../data/osm_routepoints.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            osm_id =  row['stop_id'].split(':')[-1]
            if osm_id not in osm_dedup_id_list:
                osm_dedup_id_list.append(osm_id)
            else:
                continue #we only check each stop once (even if it can have multiple errors)
            error = {"id" : osm_id}
            if not row['stop_ref:FR:STIF']:
                continue
            osm_ref = row['stop_ref:FR:STIF']
            all_osm_ref = osm_ref.split(';')
            noexistant_ref = [elem for elem in all_osm_ref if elem not in ref_STIF_list]
            if noexistant_ref: 
                continue #already covered by the test on the stops
            lines_ok_for_this_ref = [all_ref_STIF[a_ref] for a_ref in all_osm_ref if a_ref in ref_STIF_list]
            flat_list_lines_ok = [item for sublist in lines_ok_for_this_ref for item in sublist]
            if not flat_list_lines_ok :
                continue

            osm_line_ref = row['line_ref:FR:STIF']
            if osm_line_ref not in all_lines_ref_STIF:
                continue #already covered by the test on the lines
            if osm_line_ref not in flat_list_lines_ok:
                label = "Pour cet arrêt de ref:FR:STIF {} l'association avec la ligne {} est à vérifier".format(osm_ref, osm_line_ref)
                label += " https://ref-lignes-stif.5apps.com/stop.html?osm_stop_id={}".format(error['id'])
                error['label'] = label
                error['ref:FR:STIF'] = osm_ref
                error['lat'], error['lon'] = row['lat'], row['lon']
                errors.append(error)
    return errors

if __name__ == '__main__':
    stop_errors = generate_osmose_errors_for_stops()
    print("Il y a {} erreurs sur les arrêts".format(len(stop_errors)))

    routepoints_errors = generate_osmose_errors_for_routepoints()
    print("Il y a {} erreurs sur les routepoints".format(len(routepoints_errors)))
