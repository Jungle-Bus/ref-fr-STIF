# Audit comparatif OSM / STIF

:warning::construction: c'est pas fini ! :construction::warning:

Afin de gommer les divergences de modélisation, au lieu de considérer des arrêts, on travaillera sur des routepoints.

Un routepoint est un object fictif qui représente un arrêt desservi par une ligne dans une direction.

Si deux lignes s'arrêtent à un arrêt, il est représenté par deux routepoints.

Schéma attendu pour les routepoints :
* un id d'arrêt
* un code de ligne (de parcours en fait)
* terminus de ligne (de parcours en fait)
* code STIF de la ligne
* code STIF de l'arrêt
* nom de l'arrêt
* des infos complémentaires sur l'arrêt (coordonnées, accessibilité, etc)
* des infos complémentaires sur l'arrêt (réseau, etc)
