#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ref_FR_STIF_arrets
import ref_FR_STIF_lignes

import xmltodict
import datetime
from copy import deepcopy


def create_osmose_xml_stops(errors):
    with open('osmose_issues_template.xml', 'r') as f:
        doc = xmltodict.parse(f.read())

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    doc['analysers']['@timestamp'] = now
    doc['analysers']['analyser']['@timestamp'] = now
    doc['analysers']['analyser']['class']['@item'] = "8042"
    doc['analysers']['analyser']['class']['@tag'] = "transport en commun"
    doc['analysers']['analyser']['class']['@id'] = "2" 
    doc['analysers']['analyser']['class']['@level'] = "3"
    doc['analysers']['analyser']['class']['@source'] = "https://github.com/Jungle-Bus/ref-fr-STIF/tree/master/osmose"
    doc['analysers']['analyser']['class']['@resource'] = "https://ref-lignes-stif.5apps.com/"
    doc['analysers']['analyser']['class']['classtext'][0]['@lang'] = "en"
    doc['analysers']['analyser']['class']['classtext'][0][
        '@title'] = "Wrong or missing tag on a public transport stop in Île-de-France"
    doc['analysers']['analyser']['class']['classtext'][1]['@lang'] = "fr"
    doc['analysers']['analyser']['class']['classtext'][1][
        '@title'] = "tag à vérifier sur un arrêt de transport en commun d'Île-de-France"

    for error in errors :
        current_osmose_error = deepcopy(doc['analysers']['analyser']['error'][1])
        current_osmose_error['@class'] = '2'
        current_osmose_error['node']['@id'] = error['id']
        current_osmose_error['location']['@lat'] = error['lat']
        current_osmose_error['location']['@lon'] = error['lon']
        current_osmose_error['text']['@lang'] = "fr"
        current_osmose_error['text']['@value'] = error['label']
        current_osmose_error['fixes']['fix']['node']['@id'] = error['id']
        current_osmose_error['fixes']['fix']['node']['tag']['@k'] = 'ref:FR:STIF'

        doc['analysers']['analyser']['error'].append(current_osmose_error)

    # remove the template errors
    del doc['analysers']['analyser']['error'][0]
    del doc['analysers']['analyser']['error'][0]

    return xmltodict.unparse(doc, pretty=True)


def create_osmose_xml_lines(errors):
    with open('osmose_issues_template.xml', 'r') as f:
        doc = xmltodict.parse(f.read())

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    doc['analysers']['@timestamp'] = now
    doc['analysers']['analyser']['@timestamp'] = now
    doc['analysers']['analyser']['class']['@item'] = "8042"
    doc['analysers']['analyser']['class']['@tag'] = "transport en commun"
    doc['analysers']['analyser']['class']['@source'] = "https://github.com/Jungle-Bus/ref-fr-STIF/tree/master/osmose"
    doc['analysers']['analyser']['class']['@resource'] = "https://ref-lignes-stif.5apps.com/"
    doc['analysers']['analyser']['class']['@id'] = "1"
    doc['analysers']['analyser']['class']['@level'] = "3"
    doc['analysers']['analyser']['class']['classtext'][0]['@lang'] = "en"
    doc['analysers']['analyser']['class']['classtext'][0][
        '@title'] = "Wrong or missing tag on a route_master relation (public transport line) in Île-de-France"
    doc['analysers']['analyser']['class']['classtext'][1]['@lang'] = "fr"
    doc['analysers']['analyser']['class']['classtext'][1][
        '@title'] = "tag manquant ou à vérifier sur une relation route_master (ligne de transport en commun) d'Île-de-France"
        
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
    stop_errors = ref_FR_STIF_arrets.generate_osmose_errors_for_stops()
    print("Il y a {} erreurs sur les arrêts".format(len(stop_errors)))

    routepoints_errors = ref_FR_STIF_arrets.generate_osmose_errors_for_routepoints()
    print("Il y a {} erreurs sur les routepoints".format(len(routepoints_errors)))

    xml = create_osmose_xml_stops(stop_errors + routepoints_errors)
    with open("../data/osmose_stops.xml", "w") as xml_out_file:
        xml_out_file.write(xml)

    lines_errors, lines_improv = ref_FR_STIF_lignes.generate_osmose_errors_for_lines()
    print("Il y a {} erreurs sur les lignes".format(len(lines_errors)))
    print("Il y a {} améliorations possibles sur les lignes à partir de l'open data".format(len(lines_improv)))

    xml = create_osmose_xml_lines(lines_errors)
    with open("../data/osmose_lines.xml", "w") as xml_out_file:
        xml_out_file.write(xml)
    
    #TODO add improvements for lines too
