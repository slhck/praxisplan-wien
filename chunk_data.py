#!/usr/bin/env python3
#
# chunk the data into smaller files.

import hashlib
import json
import os
import re
import shutil


def get_district(address):
    match = re.match(r"(\d+)\.,", address)
    return match.group(1) if match else "unknown"


def write_chunk(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def sanitize_filename(name):
    # # Replace umlauts and ß
    # name = (
    #     name.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    # )
    # # Remove non-ASCII characters
    # name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("ASCII")
    # # Replace spaces and other non-alphanumeric characters with underscores
    # name = re.sub(r"[^\w\-_\.]", "_", name)
    # # Remove consecutive underscores
    # name = re.sub(r"_+", "_", name)
    # # Trim underscores from start and end
    # return name.strip("_")
    # --> does not work because underscores determine the split characters

    # just use an md5 hash of the name
    return hashlib.md5(name.encode()).hexdigest()


def main():
    with open("data.json", "r") as f:
        data = json.load(f)

    # Delete and recreate output directory
    if os.path.exists("data_chunks"):
        shutil.rmtree("data_chunks")
    os.makedirs("data_chunks", exist_ok=True)

    # Chunk the data by last name's first letter and district
    name_chunks = {}
    # Chunk the data by Fach and district
    fach_chunks = {}
    # Keep track of original Fach names
    fach_mapping = {}

    for feature in data["features"]:
        properties = feature["properties"]
        last_name = properties["NAME"].split()[-1]
        first_letter = last_name[0].upper()
        district = get_district(properties["ADRESSE"])
        fach = properties["FACH"]
        sanitized_fach = sanitize_filename(fach)

        name_key = f"name_{first_letter}_{district}"
        fach_key = f"fach_{sanitized_fach}_{district}"

        if name_key not in name_chunks:
            name_chunks[name_key] = []
        name_chunks[name_key].append(feature)

        if fach_key not in fach_chunks:
            fach_chunks[fach_key] = []
        fach_chunks[fach_key].append(feature)

        # Store the mapping between sanitized and original Fach names
        fach_mapping[sanitized_fach] = fach

    # Write chunks to files
    for key, chunk_data in name_chunks.items():
        write_chunk(f"data_chunks/chunk_{key}.json", chunk_data)
    for key, chunk_data in fach_chunks.items():
        write_chunk(f"data_chunks/chunk_{key}.json", chunk_data)

    # Create an index file
    index = {
        "total_doctors": len(data["features"]),
        "name_chunks": list(name_chunks.keys()),
        "fach_chunks": list(fach_chunks.keys()),
        "fach_mapping": fach_mapping,
    }

    with open("data_chunks/index.json", "w") as f:
        json.dump(index, f, indent=4)

    print(f"Data chunked into {len(name_chunks) + len(fach_chunks)} files.")


if __name__ == "__main__":
    main()
