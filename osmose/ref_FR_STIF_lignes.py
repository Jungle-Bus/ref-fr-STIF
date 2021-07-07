#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from collections import Counter

def get_lines_from_csv(file_name):
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def extract_common_values_by_networks(osm_lines, opendata_lines):
    networks = {}
    operators = {}
    for an_opendata_line in opendata_lines:
        nav_network = networks.setdefault(an_opendata_line['agency_id'], [])
        nav_operator = operators.setdefault(an_opendata_line['agency_id'], [])
        osm_match = [a_line for a_line in osm_lines if a_line['osm:ref:FR:STIF']
                     == "IDFM:{}".format(an_opendata_line['route_id'])]
        if (osm_match):
            nav_network.append(osm_match[0]['network'])
            nav_operator.append(osm_match[0]['operator'])
    return {"networks": networks, "operators": operators}

def get_most_common_value(stat_info, tag, opendata_network_id):
    c = Counter(stat_info[tag + 's'][opendata_network_id])
    return c.most_common(1)[0][0]

def map_modes(opendata_mode):
    mapping = {"3": "bus", "2": "train",
               "0": "tram", "1": "subway"}
    return mapping[opendata_mode]

def get_errors(osm_lines, opendata_lines, stats, line_coords):
    errors = []
    improvements = []
    opendata_deduplicated = []
    for an_osm_line in osm_lines:
        an_osm_line['osm_id'] = an_osm_line['line_id'].split(':')[-1]

        line_with_coords = [a_line for a_line in line_coords if a_line['line_id'] == an_osm_line['line_id']]
        if not line_with_coords:
            line_with_coords = [{'lon': '2.249699', 'lat': '48.562577'}]
        an_osm_line['latitude'], an_osm_line['longitude'] = line_with_coords[0]['lat'], line_with_coords[0]['lon']

        if not an_osm_line['osm:ref:FR:STIF']:
            continue

        osm_ref = an_osm_line['osm:ref:FR:STIF']

        if osm_ref not in opendata_deduplicated:
            opendata_deduplicated.append(osm_ref)
        else:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "Il y a plusieurs lignes dans OSM qui ont ce même ref:FR:STIF ({})".format(
                an_osm_line['osm:ref:FR:STIF'])
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        
        if not osm_ref.startswith("C"):
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "L'attribut ref:FR:STIF ({}) est invalide, il devrait commencer par un C.".format(
                osm_ref)
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue

        try :
            int(osm_ref[1:])
        except ValueError :
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "L'attribut ref:FR:STIF ({}) est invalide, il devrait être constitué d'un C suivi d'une série de chiffres.".format(
                osm_ref)
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue 

        opendata_matching_lines = [
            a_line for a_line in opendata_lines if an_osm_line['osm:ref:FR:STIF'] == a_line['route_id'].replace("IDFM:","")]
        if not opendata_matching_lines:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "Ce ref:FR:STIF ({}) n'existe pas ou plus dans les données opendata d'IDFM (ex-STIF)".format(
                an_osm_line['osm:ref:FR:STIF'])
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        opendata_line = opendata_matching_lines[0]

        if not an_osm_line['colour']:
            error = {"id": an_osm_line['osm_id']}
            opendata_color = "#{}".format(opendata_line['route_color'].lower())
            error['label'] = "Couleur (tag colour) manquante pour cette ligne"
            error['fix'] = [{"key": "colour", "value": opendata_color}]
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            improvements.append(error)
            continue

        if not an_osm_line['network']:
            error = {"id": an_osm_line['osm_id']}
            fix = get_most_common_value(
                stats, "network", opendata_line['agency_id'])
            error['label'] = "Réseau de transport (tag network) manquant pour cette ligne."
            if fix != "":
                error['fix'] = [{"key": "network", "value": fix}]
                error['label'] = "Réseau de transport (tag network) manquant pour cette ligne. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            improvements.append(error)
            continue

        if not an_osm_line['operator']:
            error = {"id": an_osm_line['osm_id']}
            fix = get_most_common_value(
                stats, "operator", opendata_line['agency_id'])
            error['label'] = "Opérateur (tag operator) manquant pour cette ligne"
            if fix != "":
                error['fix'] = [{"key": "operator", "value": fix}]
                error['label'] = "Opérateur (tag operator) manquant pour cette ligne. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            improvements.append(error)
            continue

        if not an_osm_line['code']:
            error = {"id": an_osm_line['osm_id']}
            fix = opendata_line['route_short_name']
            error['label'] = "Numéro de ligne (tag ref) manquant. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            error['fix'] = [{"key": "ref", "value": fix}]
            improvements.append(error)
            continue

        if not an_osm_line['mode']:
            error = {"id": an_osm_line['osm_id']}
            fix = map_modes(opendata_line['route_type'])
            error['label'] = "la relation n'a pas de tag route_master. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            error['fix'] = [{"key": "route_master", "value": fix}]
            improvements.append(error)
            
    return errors, improvements

def generate_osmose_errors_for_lines():
    osm_lines = get_lines_from_csv('../data/lignes.csv')
    opendata_lines = get_lines_from_csv('../data/gtfs_routes.txt')
    osm_line_coords = get_lines_from_csv('../data/osmose_relations_with_coord.csv')

    stats = extract_common_values_by_networks(osm_lines, opendata_lines)
    #print(get_most_common_value(stats, "network", "56"))
    #print(get_most_common_value(stats, "operator", "56"))

    errors = get_errors(osm_lines, opendata_lines, stats, osm_line_coords)
    return errors

if __name__ == '__main__':
    errors, improv = generate_osmose_errors_for_lines()
    print("Il y a {} erreurs sur les lignes".format(len(errors)))
    print("Il y a {} améliorations possibles sur les lignes à partir de l'open data".format(len(improv)))

    # osm_lines = get_lines_from_csv('../data/lignes.csv')
    # opendata_lines = get_lines_from_csv('../data/gtfs_routes.txt')
    # osm_line_coords = get_lines_from_csv('../data/osmose_relations_with_coord.csv')
    #
    # stats = extract_common_values_by_networks(osm_lines, opendata_lines)
    # for a_stat in stats['networks']:
    #     all_networks = list(set(stats['networks'][a_stat]))
    #     if len(all_networks) == 0:
    #         print("pas trouvé - " + a_stat)
    #     if len(all_networks) > 1:
    #         print("plusieurs solutions pour " + a_stat)
    #         print(all_networks)
