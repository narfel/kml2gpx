"Convert kml file from google earth to gpx file"
import argparse
import sys
from datetime import datetime, timedelta

# create argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="Input KML file")
parser.add_argument("-o", type=str, help="Output KML file")

args = parser.parse_args()
input_file = args.i or "input.kml"
output_file = args.o or "output.gpx"

# test input file for LineString (denotes path object) and count
INSTANCES = 0
try:
    with open(input_file, encoding="utf8") as preprocess:
        for num, line in enumerate(preprocess, 1):
            if "<LineString>" in line:
                INSTANCES = INSTANCES + 1
                if INSTANCES == 1:
                    # coordinates are three lines after LineString designator
                    coordLine = num + 3
            if INSTANCES == 1 and num == coordLine:
                coordinates = line
except (FileNotFoundError, PermissionError) as exc:
    print(f"Could not open the file: {input_file}. Error: {exc}")
    sys.exit()

# validate input file has one path object
if INSTANCES == 0:
    print("No paths found in KML")
    sys.exit()
if INSTANCES > 1:
    print("Whoops, too many paths in the KML. Try exporting one path at a time")
    sys.exit()

# clean up coordinates data
coordinates = coordinates.lstrip("\t")
# split into tuples
coordinates = coordinates.split(" ")
del coordinates[-1]

with open(output_file, "w+", encoding="utf8") as output:
    # populate header
    output.write('<?xml version="1.0" encoding="UTF-8"?>\r\n')
    output.write(
        "<!-- Time data is conversion date iterated by 1s per point since "
        "no time data is contained in kml and many apps require it -->\r\n"
        '<gpx version="1.1" creator="Google Earth" '
        'xmlns="http://www.topografix.com/GPX/1/1" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
        'http://www.topografix.com/GPX/1/1/gpx.xsd">\r\n'
    )
    output.write(f"\r\n<trk>\r\n <name>{output_file}</name>\r\n <trkseg>\r\n")

    today = datetime.now()  # add dummy time based on current date
    second = timedelta(seconds=1)  # iterate each waypoint by one second

    # iterate through coordinate array and write each line reversing lat/lon
    for element in coordinates:
        lat, lon, ele = element.split(",")
        output.write(f'  <trkpt lat="{lon}" lon="{lat}"><ele>{ele}</ele>')
        output.write(
            f"<time>{today.replace(microsecond=0).isoformat()}Z</time></trkpt>\r\n"
        )
        today += second

    # write closeout data
    output.write(" </trkseg>\r\n</trk>\r\n\r\n</gpx>\r\n")

print(f"Gpx track with {len(coordinates)} points exported to {output_file}")
