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
    # Open the GPX file and parse its contents
    with open(gpx_file, "r") as file:
        gpx = gpxpy.parse(file)

    points_list = list()
    points_index = 0

    # Loop through each track in the GPX file
    for track in gpx.tracks:
        # Loop through each segment in the track
        for segment in track.segments:
            # Loop through each point in the segment
            unique_points_dict = dict()
            for point in tqdm(segment.points, desc="Getting all points"):
                current_point = (point.latitude, point.longitude, point.elevation)
                if current_point not in unique_points_dict:
                    # When the point is unique, we add it to the dictionary and the list
                    unique_points_dict[current_point] = True
                    points_list.append(
                        geo2decart(point.latitude, point.longitude, point.elevation, points_index))
                    points_index += 1

    return points_list


def gen_json(data_list, output_json_file):
    """
    Writes the provided data list to a JSON file.

    :param output_json_file: File path or file-like object for the output JSON file.
    :param data_list: List of data to be written to the JSON file.
    """
    with open(output_json_file, "w") as file:
        json.dump(data_list, file)


def set_zero_x_y(orig_list):
    """
    Sets the first point to (0;0;0).

    :param orig_list: Original list with track point coordinates, where the first point is located outside the world.
    :return: List with track point coordinates, where the first point has coordinates (0;0;0).
    """
    zero_x = orig_list[0]['x']
    zero_y = orig_list[0]['y']
    zero_z = orig_list[0]['z']

    for item in tqdm(orig_list, desc="Flattening"):
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
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'{logo}\nConverter from GPX to JSON'
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.0.2a",
                        help="show program version and exit")
    parser.add_argument("--gpx", required=True, help="specify the path to the GPX file")
    parser.add_argument("--json", required=True, help="specify the path to the JSON file")
    # If the main script is called without arguments, display help.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    print(logo)
    gen_json(set_zero_x_y(parse_gpx(args.gpx)), args.json)
