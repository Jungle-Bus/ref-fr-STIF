#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

NETWORK_MAPPINGS = {
    "Paris Saclay" : "Paris-Saclay",
    "Paris-Saclay Mobilités" : "Paris-Saclay",
    "Saint Germain Boucles de Seine" : "Saint-Germain Boucles de Seine",
    "Cœur d’Essonne" : "Cœur d'Essonne",
    "Brie et 2 Morin" : "Brie et Deux Morin",
    "Seine et Marne Express" : "Seine-et-Marne Express",
    "Vallée Grand Sud Paris" : "Vallée Sud Bus",
    "Evry Centre Essonne" : "Évry Centre Essonne",
    "Haut Val d’Oise" : "Haut Val d'Oise",
    "Lignes Île-de-France Ouest" : "Île-de-France Ouest",
}

OPERATOR_MAPPINGS = {
    "ADP" : "Aéroports de Paris",
    "Aéroport Paris-Beauvais / SAGEB" : "Aéroport Paris-Beauvais",
    "STBC" : "Société des transports du bassin chellois",
    "Mobicité" : "MobiCité",
    "TISSE": "Keolis TISSE",
    "Keolis Vallée de l’Oise" : "Keolis Vallée de l'Oise",
    "N4 Mobilités" : "Transdev N4 Mobilités",
    "Cars Rose" : "Transdev Les Cars Rose",
    "TRA" : "Transdev TRA",
    "Transdev Boucle des Lys" : "Transdev Île-de-France Boucle des Lys",
    "Transdev Brie et 2 Morin" : "Transdev Brie et Deux Morin",
    "Transdev Senart" : "Transdev Sénart",
    "RD Bièvre" : "RATP Cap Bièvre",
    "RD Mantois" : "RATP Cap Mantois",
    "RD Saclay" : "RATP Cap Saclay",
}

MODE_MAPPINGS = {
    "metro": "subway"
}

def get_lines_from_csv(file_name):
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_errors(osm_lines, opendata_lines, line_coords):
    errors = []
    improvements = []
    opendata_deduplicated = []
    for an_osm_line in osm_lines:
        an_osm_line['osm_id'] = an_osm_line['line_id'].split('r')[-1]

        line_with_coords = [a_line for a_line in line_coords if a_line['line_id'] == an_osm_line['line_id']]
        if not line_with_coords:
            line_with_coords = [{'longitude': '2.249699', 'latitude': '48.562577'}]
        an_osm_line['latitude'], an_osm_line['longitude'] = line_with_coords[0]['latitude'], line_with_coords[0]['longitude']

        if not an_osm_line['ref:FR:STIF']:
            continue

        osm_ref = an_osm_line['ref:FR:STIF']

        if osm_ref not in opendata_deduplicated:
            opendata_deduplicated.append(osm_ref)
        else:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "Il y a plusieurs lignes dans OSM qui ont ce même ref:FR:STIF ({})".format(
                an_osm_line['ref:FR:STIF'])
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        
        if not osm_ref.startswith("C"):
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "L'attribut ref:FR:STIF ({}) est invalide, il devrait commencer par un C.".format(
                osm_ref)
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue

        if not osm_ref[1:].isnumeric():
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "L'attribut ref:FR:STIF ({}) est invalide, il devrait être constitué d'un C suivi d'une série de chiffres.".format(
                osm_ref)
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue 

        opendata_matching_lines = [
            a_line for a_line in opendata_lines if an_osm_line['ref:FR:STIF'] == a_line['ID_Line']]
        if not opendata_matching_lines:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "Ce ref:FR:STIF ({}) n'existe pas ou plus dans les données opendata d'IDFM (ex-STIF)".format(
                an_osm_line['ref:FR:STIF'])
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        opendata_line = opendata_matching_lines[0]

        opendata_network = opendata_line["NetworkName"]
        if opendata_line["NetworkName"] in NETWORK_MAPPINGS:
            opendata_network = NETWORK_MAPPINGS[opendata_line["NetworkName"]]
        if not an_osm_line['network']:
            error = {"id": an_osm_line['osm_id']}
            error['fix'] = [{"key": "network", "value": opendata_network}]
            error['label'] = "Réseau de transport (tag network) manquant pour cette ligne. Valeur probable : " + opendata_network
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        elif an_osm_line['network'] != opendata_network :
            if opendata_network in ["", "ValBus", "Parisis", "Sit'bus", "Conflans Achères", "Chavilbus"]:
                # ce sont des réseaux qui ont vocation à disparaitre, donc OSEF
                pass
            else : 
                error = {"id": an_osm_line['osm_id']}
                error['fix'] = [{"key": "network", "value": opendata_network}]
                error["network"] = opendata_network
                error['old'] = an_osm_line['network']
                error['label'] = "Réseau de transport (tag network) erroné pour cette ligne. Valeur probable : " + opendata_network
                error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
                errors.append(error)
                continue


        opendata_operator = opendata_line["OperatorName"]
        if opendata_line["OperatorName"] in OPERATOR_MAPPINGS:
            opendata_operator = OPERATOR_MAPPINGS[opendata_line["OperatorName"]]
        if not an_osm_line['operator']:
            error = {"id": an_osm_line['osm_id']}
            error['fix'] = [{"key": "operator", "value": opendata_operator}]
            error['label'] = "Opérator de transport (tag operator) manquant pour cette ligne. Valeur probable : " + opendata_operator
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        elif an_osm_line['operator'] != opendata_operator :
            if opendata_operator in ["", "SNCF", "Magical Shuttle"]:
                pass
            else :           
                error = {"id": an_osm_line['osm_id']}
                error['fix'] = [{"key": "operator", "value": opendata_operator}]
                error["network"] = opendata_network
                error['old'] = an_osm_line['operator']
                error['label'] = "Opérateur de transport (tag operator) erroné pour cette ligne. Valeur probable : " + opendata_operator
                error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
                errors.append(error)
                continue

        opendata_code = opendata_line["ShortName_Line"]
        if not an_osm_line['code']:
            error = {"id": an_osm_line['osm_id']}
            error['fix'] = [{"key": "code", "value": opendata_code}]
            error['label'] = "Numéro de ligne (tag ref) manquant pour cette ligne. Valeur probable : " + opendata_code
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            errors.append(error)
            continue
        elif an_osm_line['code'] != opendata_code :
            if opendata_code in [""] or not opendata_code.isnumeric():
                pass
            else :           
                error = {"id": an_osm_line['osm_id']}
                error['fix'] = [{"key": "code", "value": opendata_code}]
                error["network"] = opendata_network
                error['old'] = an_osm_line['code']
                error['label'] = "Numéro de ligne (tag ref) erroné pour cette ligne. Valeur probable : " + opendata_code
                error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
                errors.append(error)
                continue

        opendata_mode = opendata_line["TransportMode"]
        if opendata_line["TransportMode"] in MODE_MAPPINGS:
            opendata_mode = MODE_MAPPINGS[opendata_line["TransportMode"]]
        if not an_osm_line['mode']:
            error = {"id": an_osm_line['osm_id']}
            error['label'] = "la relation n'a pas de tag route_master. Valeur probable : " + opendata_mode
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            error['fix'] = [{"key": "route_master", "value": opendata_mode}]
            errors.append(error)
            continue
    
        if not an_osm_line['colour']:
            error = {"id": an_osm_line['osm_id']}
            opendata_color = "#{}".format(opendata_line['TextColourWeb_hexa'].lower())
            if opendata_color in ["#ffffff", "#000000"]:
                continue
            error['label'] = "Couleur (tag colour) manquante pour cette ligne"
            error['fix'] = [{"key": "colour", "value": opendata_color}]
            error['latitude'], error['longitude'] = an_osm_line['latitude'], an_osm_line['longitude']
            improvements.append(error)            
            
    return errors, improvements

def generate_osmose_errors_for_lines():
    osm_lines = get_lines_from_csv('../data/lignes.csv')
    opendata_lines = get_lines_from_csv('../data/opendata_lines_referential.csv')
    osm_line_coords = get_lines_from_csv('../data/osmose_relations_with_coord.csv')

    errors = get_errors(osm_lines, opendata_lines, osm_line_coords)
    return errors

if __name__ == '__main__':
    errors, improv = generate_osmose_errors_for_lines()
    print("Il y a {} erreurs sur les lignes".format(len(errors)))
    print("Il y a {} améliorations possibles sur les lignes à partir de l'open data".format(len(improv)))

    with open('errors.csv', 'w') as out_file:
        csv_writer = csv.DictWriter(out_file, delimiter=',', fieldnames=errors[0].keys())
        csv_writer.writeheader()
        for row in errors:
            csv_writer.writerow(row)




