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
