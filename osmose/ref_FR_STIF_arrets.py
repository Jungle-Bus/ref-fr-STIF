#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def generate_osmose_errors_for_stops():
    errors = []
    ref_STIF_list = []
    with open('../data/gtfs_stop_extensions.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader :
            ref_STIF_list.append(row["ZDEr_ID_REF_A"])

    with open('../data/osm-transit-extractor_stop_points.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            error = {"id" : row['stop_point_id'].split(':')[-1] }
            if not row['osm:ref:FR:STIF']:
                continue
            osm_ref = row['osm:ref:FR:STIF']
            if ';' in osm_ref :
                for a_ref in osm_ref.split(';'):
                    if a_ref.strip() not in ref_STIF_list :
                        error['label'] = "La ref:FR:STIF {} n'existe pas ou plus.".format(a_ref)
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


if __name__ == '__main__':
    generate_osmose_errors_for_stops()
