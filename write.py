"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each
of which accept an `results` stream of close approaches and a path to which
to write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""


import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results`stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should
    be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
            'designation', 'name', 'diameter_km', 'potentially_hazardous')

    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        for row in results:
            r = [row.time, row.distance, row.velocity, row.neo.designation,
                row.neo.name, row.neo.diameter, row.neo.hazardous]
            writer.writerow(r)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output
    is a list containing dictionaries, each mapping `CloseApproach`
    attributes to their values and the 'neo' key mapping to a dictionary of
    the associated NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should
     be saved.
    """
    dicts = []
    for row in results:
        print(row.neo)
        r = {'datetime_utc': datetime_to_str(row.time),
            'distance_au': row.distance, 'velocity_km_s': row.velocity,
             'designation': row._designation,
             'neo':{'designation': row.neo.designation,
             'name': row.neo.name, 'diameter_km': row.neo.diameter,
             'potentially_hazardous': row.neo.hazardous}}
        dicts.append(r)

    with open(filename, 'w') as json_file:
        json.dump(dicts, json_file, indent=4, sort_keys=False)
