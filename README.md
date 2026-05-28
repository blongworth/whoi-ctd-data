# WHOI AR61B CTD bottle data

This project builds a compact CSV of CTD rosette bottle data for the R/V Neil Armstrong AR61B cruise from the NES-LTER API.

## Usage

```bash
uv run python main.py
```

The script writes:

```text
data/ar61b_ctd_cast_data.csv
```

## Download

[Download the AR61B CTD CSV](https://raw.githubusercontent.com/blongworth/whoi-ctd-data/main/data/ar61b_ctd_cast_data.csv)

## Provenance

Source: <https://nes-lter-api.whoi.edu/>

The script downloads these public CSV endpoints for cruise `AR61B`:

- `/api/ctd/bottles/{cruise}.csv` — bottle-level CTD data
- `/api/ctd/metadata/{cruise}.csv` — cast metadata and nearest NES-LTER station
- `/api/chl/{cruise}.csv` — extracted chlorophyll measurements

## Processing

`main.py` uses pandas to:

1. Download bottle data for `AR61B`.
2. Add station names from CTD metadata (`nearest_station`).
3. Average chlorophyll replicate measurements by cruise, cast, and Niskin bottle.
4. Join chlorophyll to the bottle data.
5. Write a table with columns: timestamp, station, cast, latitude, longitude, depth, niskin bottle, temperature, salinity, oxygen, and chlorophyl.

Column mappings from the API are:

- `date` → `timestamp`
- `nearest_station` → `station`
- `cruise` + `cast` → `cast` (for example, `AR61B-5`)
- `depsm` → `depth`
- `niskin` → `niskin bottle`
- `t090c` → `temperature`
- `sal00` → `salinity`
- `sbox0mm_kg` → `oxygen`
- `chl` → `chlorophyl`
