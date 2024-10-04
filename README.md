# Praxisplan Wien

This repository contains a simple web app to search for doctors in Vienna, Austria.

## Data

The data is sourced from the [Wien.gv.at](https://www.wien.gv.at/statistik/gesundheit/arzt-und-zahnarzt/arzt-und-zahnarzt-daten.html) website.

The data format is a parent object with a `features` array. Each feature has a `geometry` object with a `Point` and a `properties` object.

Here is an example of a feature:

```json
{
  "type": "Feature",
  "id": "ARZTOGD.13040917",
  "geometry": {
    "type": "Point",
    "coordinates": [
      16.27443971,
      48.16017668
    ]
  },
  "geometry_name": "SHAPE",
  "properties": {
    "OBJECTID": 13040917,
    "NAME": "Dr. Edmund Gatterer",
    "ADRESSE": "13., Dr.-Schreber-Gasse 10",
    "FACH": "Allgemeinmedizin",
    "TELEFON": "+43 1 802 00 23 15",
    "INTERNET": "https://praxisplan.at/1344/edmund-gatterer/ordination/2",
    "SE_ANNO_CAD_DATA": null
  }
}
```

## Usage

```bash
./download_data.py
./chunk_data.py
```

Then open `index.html` in your browser.

Note: This is still using OpenStreetMap tiles, rather than the PMTiles tiles.

## License

Dataset is licensed under the [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) license.

This project is licensed under the MIT License. See the LICENSE file for details.
