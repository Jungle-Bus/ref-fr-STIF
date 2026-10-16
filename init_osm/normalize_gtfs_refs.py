#!/usr/bin/env python3

import csv
import sys

IDFM_PREFIX = "IDFM:"

# Some CSV fields (e.g. encoded geometries) can exceed the default 131072
csv.field_size_limit(sys.maxsize)

def normalize(path, gtfs_column):
    with open(path, newline='') as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return

    fieldnames = [name for name in rows[0].keys() if name != gtfs_column]

    for row in rows:
        gtfs_value = row.get(gtfs_column, '')
        if not row.get('ref:FR:STIF') and gtfs_value:
            if gtfs_value.startswith(IDFM_PREFIX):
                gtfs_value = gtfs_value[len(IDFM_PREFIX):]
            row['ref:FR:STIF'] = gtfs_value
        row.pop(gtfs_column, None)

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    csv_path, gtfs_column_name = sys.argv[1], sys.argv[2]
    normalize(csv_path, gtfs_column_name)
