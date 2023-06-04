"Convert kml file from google earth kml format to gpx file"

import re
import sys
from datetime import datetime, timedelta
from typing import List, TextIO


def write_gpx_data(output: TextIO, output_file: str, coordinates: List[str]) -> None:
    """
    Writes the GPX data to the output file.

    Args:
        output (TextIO): The output file to write to.
        output_file (str): The name of the output file.
        coordinates (List[str]): A list of string coordinates "lat,lon,ele".
    """
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\r\n',
        '<gpx version="1.1" creator="Google Earth" '
        'xmlns="http://www.topografix.com/GPX/1/1" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
        'http://www.topografix.com/GPX/1/1/gpx.xsd">\r\n',
        f"\r\n<trk>\r\n <name>{output_file}</name>\r\n <trkseg>\r\n",
    ]

    today = datetime.now()  # Add a dummy time based on the current date
    second = timedelta(seconds=1)  # Iterate each waypoint by one second

    # Iterate over the coordinate array and write coordinates reversing lat/lon
    for element in coordinates:
        lat, lon, ele = element.split(",")
        lines.extend(
            (
                f'  <trkpt lat="{lon}" lon="{lat}"><ele>{ele}</ele>',
                f"<time>{today.replace(microsecond=0).isoformat()}Z</time></trkpt>\r\n",
            )
        )
        today += second

    # Write the track segment footer and GPX footer
    lines.append(" </trkseg>\r\n</trk>\r\n\r\n</gpx>\r\n")
    output.writelines(lines)


def get_coords(input_file: str) -> str:  # sourcery skip: use-named-expression
    """
    Extracts the coordinates from a KML file.

    Args:
        input_file: String representing the path to the KML file.

    Returns:
        String representing the coordinates found in the KML file.

    Raises:
        FileNotFoundError: If the input_file does not exist.
        PermissionError: If the input_file cannot be opened due to permission issues.
    """
    try:
        with open(input_file, encoding="utf8") as f:
            file_contents = f.read()
            match = re.search(
                "<LineString>.*?<coordinates>(.*?)</coordinates>",
                file_contents,
                re.DOTALL,
            )
            if match:
                coord_str = match[1].strip()
                return coord_str
            print("No coordinates found in KML file")
            sys.exit()
    except (FileNotFoundError, PermissionError) as exc:
        print(f"Could not open the file: {input_file}. Error: {exc}")
        sys.exit()


def main() -> None:
    """
    Converts a KML file to a GPX file and exports the GPX file.

    Usage: python app.py [input_file.kml]
    """
    if len(sys.argv) != 2:
        print("Usage: python app.py [input_file.kml]")
        sys.exit()

    input_file = sys.argv[1]
    output_file = input_file.replace(".kml", ".gpx")

    coord_str = get_coords(input_file)

    # split into tuples
    coord_str = coord_str.lstrip("\t").split(" ")
    del coord_str[-1]

    with open(output_file, "w", encoding="utf8") as output:
        write_gpx_data(output, output_file, coord_str)

    print(f"Gpx track with {len(coord_str)} points exported to {output_file}")


if __name__ == "__main__":
    main()  # pragma no cover
