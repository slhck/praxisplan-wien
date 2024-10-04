#!/usr/bin/env python3
#
# Download dataset for Praxisplan and PMTiles (disabled for now)
#
# https://www.data.gv.at/katalog/dataset/fdcaabe5-0efd-4701-8fd9-49935c0d9cff#resources
# https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:ARZTOGD&srsName=EPSG:4326&outputFormat=json

import argparse
import json
import os
import subprocess
import sys


def get_bounding_box(data):
    min_lat = float("inf")
    max_lat = float("-inf")
    min_lon = float("inf")
    max_lon = float("-inf")

    for feature in data["features"]:
        lon, lat = feature["geometry"]["coordinates"]
        min_lat = min(min_lat, lat)
        max_lat = max(max_lat, lat)
        min_lon = min(min_lon, lon)
        max_lon = max(max_lon, lon)

    return {
        "min_lat": min_lat,
        "max_lat": max_lat,
        "min_lon": min_lon,
        "max_lon": max_lon,
    }


def download_data(force=False):
    if os.path.exists("data.json") and not force:
        print("data.json already exists. Skipping download.")
        return

    subprocess.run(
        [
            "curl",
            "-o",
            "data.json",
            "https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:ARZTOGD&srsName=EPSG:4326&outputFormat=json",
        ],
        check=True,
    )


def download_tiles(bounding_box, force=False):
    if os.path.exists("map.pmtiles") and not force:
        print("map.pmtiles already exists. Skipping download.")
        return

    subprocess.run(
        [
            "pmtiles",
            "extract",
            "https://build.protomaps.com/20241002.pmtiles",
            "map.pmtiles",
            f"--bbox={bounding_box['min_lon']},{bounding_box['min_lat']},{bounding_box['max_lon']},{bounding_box['max_lat']}",
        ],
        check=True,
    )


def check_command_exists(command, error_message):
    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError:
        print(f"Error: {error_message}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(
            f"Error: {command} is not installed or not in the system PATH.",
            file=sys.stderr,
        )
        print(f"{error_message}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Download data and tiles for the project."
    )
    parser.add_argument(
        "--no-download-data", action="store_true", help="Skip downloading data.json"
    )
    parser.add_argument(
        "--no-download-tiles", action="store_true", help="Skip downloading map tiles"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download of files even if they exist",
    )
    args = parser.parse_args()

    # Check if we have curl and pmtiles
    check_command_exists(
        ["curl", "--version"],
        "curl is required to download data. Please install it and try again.",
    )
    # check_command_exists(
    #     ["pmtiles", "version"],
    #     "pmtiles is required to download map tiles. Please install it and try again.",
    # )

    if not args.no_download_data:
        download_data(args.force)

    if not args.no_download_tiles:
        with open("data.json", "r") as file:
            data = json.load(file)

        bounding_box = get_bounding_box(data)
        print(f"Found bounding box: {bounding_box}")

        # print("Downloading tiles, this may take a while...")
        # download_tiles(bounding_box, args.force)

    print("Done!")


if __name__ == "__main__":
    main()
