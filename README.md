# Praxisplan Wien

This repository contains a simple web app to search for doctors in Vienna, Austria.

Contrary to the original [Praxisplan](https://www.praxisplan.at/), it has a map.

## Data

The data is sourced from the [data.gv.at](https://www.data.gv.at/katalog/dataset/arzte-standorte-wien) website.

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

We chunk these into smaller files, one for each letter of the alphabet and each district, and one for each specialty and district.

These chunks are then dynamically loaded based on the user's search query, via GZIP.

## Usage

```bash
./download_data.py
./chunk_data.py
```

Then open `index.html` in your browser.

Note: This is still using OpenStreetMap tiles, rather than the PMTiles tiles.

## Background and TODO

This was an attempt to see how much Cursor and Claude 3.5 Sonnet could do for a simple task like this, with little manual interventions in the actual code.
Some things are still TODO:

- [ ] Points in users' vicinity should be highlighted already when location is known -- but this requires a different data structure because we don't have the user's location as a district
- [ ] Some data points are obviously wrong
- [ ] Use PMTiles tiles for real offline usage
- [ ] Improve search to be a bit more fuzzy (but make it work with the chunks)
- [ ] Simplify the map style

## License

Dataset is licensed under the [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) license.

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
