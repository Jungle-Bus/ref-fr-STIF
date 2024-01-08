#!/bin/bash

set -e

# init OSM
./init_osm/init_osm.sh

# update MicrocOSM with OSM
./microcosm/microcosm.sh

# update ref-lignes-stif with OSM
./ref-lignes-stif/ref-lignes-stif.sh

# init GTFS
./init_gtfs/init_gtfs.sh

# compute routepoints with GTFS and OSM
./audit_routepoints/audit_routepoints.sh

# extract lines ref
./lines_ref/init_lines_ref.sh

# extract missing lines in OSM with GTFS and OSM
./missing_in_osm/missing_in_osm.sh

# extract focus routepoints from GTFS and OSM
#./focus/focus.sh

# extract and count linepoints from GTFS and OSM
#./check_linepoints/check_linepoints.sh

# update Osmose
./osmose/osmose.sh
