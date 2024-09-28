import argparse
import sys
import json
import pyproj
import gpxpy
from tqdm import tqdm
import time


def get_utm_zone(longitude):
    """
    Get the UTM zone based on longitude value.

    :param longitude: Longitude value.
    :return: UTM zone value corresponding to the input longitude.
    """
    # UTM (Universal Transverse Mercator) is a map projection system designed to provide
    # accurate representation of the Earth's surface. It divides the Earth into zones,
    # each spanning 6 degrees of longitude and providing equal scaling in meters for precise
    # measurement of distances and areas in GIS and cartography.
    return (int((longitude + 180) / 6) % 60) + 1


def geo2decart(lat, lon, height, index):
    """
    Converts geographic coordinates to Cartesian coordinates.

    :param lat: Latitude value.
    :param lon: Longitude value.
    :param height: Elevation or height value.
    :param index: Index or identifier for the conversion.
    :return: Cartesian coordinates corresponding to the input geographic coordinates.
    """
    # Define the input CRS
    # +proj=latlong is a projection string that specifies a geographic coordinate system
    # WGS84 -- World Geodetic System 1984 (geographic coordinates)
    input_crs = pyproj.CRS.from_proj4("+proj=latlong +datum=WGS84")

    # Define the output CRS (x, y, z)
    output_crs = pyproj.CRS.from_proj4("+proj=utm +zone=" + str(get_utm_zone(lon)) + " +datum=WGS84")

    x, y, z = pyproj.Transformer.from_crs(input_crs, output_crs).transform(lon, lat, height)

    return {'Name': 'Point_' + str(index), 'x': x, 'y': y, 'z': z}


def parse_gpx(gpx_file):
    """
    Parses a GPX (GPS Exchange Format) file and extracts relevant information.

    :param gpx_file: File path or file-like object containing GPX data.
    :return: List of points extracted from the GPX file.
    """
    gpx = gpxpy.parse(gpx_file)

    points_list = list()
    points_index = 0

    # Loop through each track in the GPX file
    for track in gpx.tracks:
        # Loop through each segment in the track
        for segment in track.segments:
            # Loop through each point in the segment
            unique_points_dict = dict()
            for point in tqdm(segment.points, desc="Getting all points", ncols=80):
                current_point = (point.latitude, point.longitude, point.elevation)
                if current_point not in unique_points_dict:
                    # When the point is unique, we add it to the dictionary and the list
                    unique_points_dict[current_point] = True
                    points_list.append(
                        geo2decart(point.latitude, point.longitude, point.elevation, points_index))
                    points_index += 1

    return points_list

def gen_json(data_list):
    """
    Converts the provided data list to a JSON-formatted string and prints it.

    :param data_list: List of data to be converted to JSON format.
    This function does not return a value but outputs the JSON string to standard output.
    """
    json_output = json.dumps(data_list)
    print(json_output)

def set_zero_x_y(orig_list):
    """
    Sets the first point to (0;0;0).

    :param orig_list: Original list with track point coordinates, where the first point is located outside the world.
    :return: List with track point coordinates, where the first point has coordinates (0;0;0).
    """
    zero_x = orig_list[0]['x']
    zero_y = orig_list[0]['y']
    zero_z = orig_list[0]['z']

    for item in tqdm(orig_list, desc="Flattening", ncols=80):
        item['x'] = item['x'] - zero_x
        item['y'] = (item['y'] - zero_y) * -1  # Mirror the track. See note below.
        item['z'] = item['z'] - zero_z

        time.sleep(0.01)  # Dark Side Accelerator

    return orig_list


if __name__ == '__main__':
    logo = """
         ██████╗ ██████╗ ██╗  ██╗██████╗      ██╗███████╗ ██████╗ ███╗   ██╗
        ██╔════╝ ██╔══██╗╚██╗██╔╝╚════██╗     ██║██╔════╝██╔═══██╗████╗  ██║
        ██║  ███╗██████╔╝ ╚███╔╝  █████╔╝     ██║███████╗██║   ██║██╔██╗ ██║
        ██║   ██║██╔═══╝  ██╔██╗ ██╔═══╝ ██   ██║╚════██║██║   ██║██║╚██╗██║
        ╚██████╔╝██║     ██╔╝ ██╗███████╗╚█████╔╝███████║╚██████╔╝██║ ╚████║
         ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                                 Project LISAPED
    """
    usage = """
    python main.py [--process] [--version]

    This script accepts GPX data from stdin for processing.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'{logo}\nConverter from GPX to JSON',
        usage=usage
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.0.4",
                        help="show program version and exit")
    parser.add_argument("--process", action="store_true", help="process GPX data from stdin")

    args = parser.parse_args()

    if args.process:
        if sys.stdin.isatty():
            print("No GPX data provided for processing. Please enter GPX data.\n")
        else:
            gpx_data = sys.stdin.read()
            if gpx_data.strip():
                gen_json(set_zero_x_y(parse_gpx(gpx_data)))
                sys.exit(0)
    else:
        print("The --process flag is not set. Data processing will not be performed.\n")

    parser.print_help(sys.stderr)
    sys.exit(1)
