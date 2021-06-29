import csv

if __name__ == "__main__":
    with open("../data/osm_routepoints.csv") as rp:
        reader = csv.DictReader(rp)
        new_rp = []
        for row in reader:
            if row['stop_ref:FR:STIF'] == "":
                continue
            if not ";" in row['stop_ref:FR:STIF']:
                new_rp.append(dict(row))
                continue
            refs = row['stop_ref:FR:STIF'].split(';')

            for ref in refs :
                new_row = dict(row)
                new_row['stop_ref:FR:STIF'] = ref.strip()
                new_rp.append(new_row)

    with open("../data/osm_routepoints_for_matching.csv", mode='w') as out_rp:
        writer = csv.DictWriter(out_rp, fieldnames = new_rp[0].keys() )
        writer.writeheader()
        for elem in new_rp:
            writer.writerow(elem)
