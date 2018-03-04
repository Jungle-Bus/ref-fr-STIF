import csv

if __name__ == "__main__":
    with open("../data/gtfs_audit_stoptime_lite.csv") as st:
        reader = csv.DictReader(st)
        trip_destinations = {}
        for row in reader:
            do_update = True
            if row["trip_id"] in trip_destinations:
                if int(row["stop_sequence"]) < int(trip_destinations[row["trip_id"]]["stop_sequence"]):
                    do_update = False
            if do_update:
                trip_destinations[row["trip_id"]] = {
                    "stop_sequence": row["stop_sequence"],
                    "stop_id": row["stop_id"]
                }
    with open("../data/gtfs_audit_trip_destinations.csv", mode='w') as out_st:
        writer = csv.writer(out_st)
        writer.writerow(["trip_id","trip_dest_id"])
        for trip_id, row in trip_destinations.items():
            writer.writerow([trip_id,row["stop_id"]])
