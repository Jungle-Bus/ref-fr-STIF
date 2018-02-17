#!/bin/bash

for file in *.txt
do
    mv $file gtfs_$file
done

mv gtfs_* ../data/
