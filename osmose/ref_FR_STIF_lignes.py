#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
import json
import xmltodict
import datetime
from collections import Counter
from copy import deepcopy


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
        osm_match = [a_line for a_line in osm_lines if a_line['osm:ref:FR:STIF:ExternalCode_Line']
                     == an_opendata_line['route_id']]
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
    opendata_deduplicated = []
    for an_osm_line in osm_lines:
        an_osm_line['osm_id'] = an_osm_line['line_id'].split(':')[-1]

        line_with_coords = [a_line for a_line in line_coords if a_line['line_id'] == an_osm_line['line_id']]
        if not line_with_coords:
            line_with_coords = [{'lon': '2.249699', 'lat': '48.562577'}]
        an_osm_line['latitude'], an_osm_line['longitude'] = line_with_coords[0]['lat'], line_with_coords[0]['lon']

        if not an_osm_line['osm:ref:FR:STIF:ExternalCode_Line']:
            continue

        if an_osm_line['osm:ref:FR:STIF:ExternalCode_Line'] not in opendata_deduplicated:
            opendata_deduplicated.append(
                an_osm_line['osm:ref:FR:STIF:ExternalCode_Line'])
        else:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "Il y a plusieurs lignes dans OSM qui ont ce même ref:FR:STIF:ExternalCode_Line ({})".format(
                an_osm_line['osm:ref:FR:STIF:ExternalCode_Line'])
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)

        opendata_matching_lines = [
            a_line for a_line in opendata_lines if an_osm_line['osm:ref:FR:STIF:ExternalCode_Line'] == a_line['route_id']]
        if not opendata_matching_lines:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "Ce ref:FR:STIF:ExternalCode_Line ({}) n'existe pas ou plus dans les données opendata du STIF".format(
                an_osm_line['osm:ref:FR:STIF:ExternalCode_Line'])
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        opendata_line = opendata_matching_lines[0]

        if not an_osm_line['network']:
            error = {"id": an_osm_line['osm_id']}
            fix = get_most_common_value(
                stats, "network", opendata_line['agency_id'])
            error['label'] = "la relation n'a pas de tag network."
            if fix != "":
                error['fix'] = [{"key": "network", "value": fix}]
                error['label'] = "la relation n'a pas de tag network. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)

        if not an_osm_line['operator']:
            error = {"id": an_osm_line['osm_id']}
            fix = get_most_common_value(
                stats, "operator", opendata_line['agency_id'])
            error['label'] = "la relation n'a pas de tag operator."
            if fix != "":
                error['fix'] = [{"key": "operator", "value": fix}]
                error['label'] = "la relation n'a pas de tag operator. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)

        if not an_osm_line['code']:
            error = {"id": an_osm_line['osm_id']}
            fix = opendata_line['code']
            error['label'] = "la relation n'a pas de tag ref. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            error['fix'] = [{"key": "ref", "value": fix}]
            errors.append(error)

        if not an_osm_line['mode']:
            error = {"id": an_osm_line['osm_id']}
            fix = map_modes(opendata_line['route_type'])
            error['label'] = "la relation n'a pas de tag route_master. Valeur probable : " + fix
            error['lat'], error['lon'] = an_osm_line['latitude'], an_osm_line['longitude']
            error['fix'] = [{"key": "route_master", "value": fix}]
            errors.append(error)

    return errors


def create_osmose_xml(errors):
    with open('osmose_issues_template.xml', 'r') as f:
        doc = xmltodict.parse(f.read())

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    doc['analysers']['@timestamp'] = now
    doc['analysers']['analyser']['@timestamp'] = now
    doc['analysers']['analyser']['class']['@item'] = "8042"
    doc['analysers']['analyser']['class']['@tag'] = "transport en commun"
    doc['analysers']['analyser']['class']['@id'] = "1"
    doc['analysers']['analyser']['class']['@level'] = "3"
    doc['analysers']['analyser']['class']['classtext']['@lang'] = "fr"
    doc['analysers']['analyser']['class']['classtext'][
        '@title'] = "tag manquant sur une relation route_master (ligne de transport en commun)"

    for error in errors:
        current_osmose_error = deepcopy(
            doc['analysers']['analyser']['error'][0])
        current_osmose_error['relation']['@id'] = error['id']
        current_osmose_error['location']['@lat'] = error['lat']
        current_osmose_error['location']['@lon'] = error['lon']
        current_osmose_error['text']['@lang'] = "fr"
        current_osmose_error['text']['@value'] = error['label']
        current_osmose_error['fixes']['fix']['relation']['@id'] = error['id']
        if 'fix' in error:
            current_osmose_error['fixes']['fix']['relation']['tag']['@k'] = error['fix'][0]['key'] if 'key' in error['fix'][0] else ''
            current_osmose_error['fixes']['fix']['relation']['tag']['@v'] = error['fix'][0]['value'] if 'key' in error['fix'][0] else ''
        else:
            del current_osmose_error['fixes']

        doc['analysers']['analyser']['error'].append(current_osmose_error)

    # remove the template errors
    del doc['analysers']['analyser']['error'][0]
    del doc['analysers']['analyser']['error'][0]

    return xmltodict.unparse(doc, pretty=True)



if __name__ == '__main__':
    osm_lines = get_lines_from_csv('../data/lignes.csv')
    opendata_lines = get_lines_from_csv('../data/gtfs_routes.txt')
    osm_line_coords = get_lines_from_csv('../data/osmose_relations_with_coord.csv')

    stats = extract_common_values_by_networks(osm_lines, opendata_lines)
    #print(get_most_common_value(stats, "network", "56"))
    #print(get_most_common_value(stats, "operator", "56"))

    errors = get_errors(osm_lines, opendata_lines, stats, osm_line_coords)

    xml = create_osmose_xml(errors)
    print("Il y a {} erreurs".format(len(errors)))

    with open("../data/osmose_lines.xml", "w") as xml_out_file:
        xml_out_file.write(xml)
