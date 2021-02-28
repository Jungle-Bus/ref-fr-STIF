#!/bin/bash

set -e

# init OSM
./init_osm/init_osm.sh

# update MicrocOSM with OSM
./microcosm/microcosm.sh

# update ref-lignes-stif with OSM
factotum run ref-lignes-stif/ref-lignes-stif.factfile

# init GTFS
./init_gtfs/init_gtfs.sh

# compute routepoints with GTFS and OSM
factotum run audit_routepoints/audit_routepoints.factfile

# extract missing lines in OSM with GTFS and OSM
factotum run missing_in_osm/missing_in_osm.factfile

# extract focus routepoints from GTFS and OSM
factotum run focus/focus.factfile

# update Osmose
factotum run osmose/osmose.factfile