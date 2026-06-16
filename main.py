from pathlib import Path

import pandas as pd

BASE_URL = "https://nes-lter-api.whoi.edu/api"
CRUISES = ("AR61B",)
OUTFILE = Path("data/ar61b_ctd_cast_data.csv")


def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(f"{BASE_URL}{path}")


def cruise_table(cruise: str) -> pd.DataFrame:
    bottles = read_csv(f"/ctd/bottles/{cruise}.csv")
    metadata = read_csv(f"/ctd/metadata/{cruise}.csv")[["cast", "nearest_station"]]
    chlorophyll = read_csv(f"/chl/{cruise}.csv")

    chlorophyll = (
        chlorophyll.groupby(["cruise", "cast", "niskin"], as_index=False)["chl"]
        .mean()
        .rename(columns={"chl": "chlorophyll"})
    )

    table = bottles.merge(metadata, on="cast", how="left").merge(
        chlorophyll, on=["cruise", "cast", "niskin"], how="left"
    )

    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(table["date"], utc=True),
            "station": table["nearest_station"],
            "cast": table["cast"],
            "latitude": table["latitude"],
            "longitude": table["longitude"],
            "depth": table["depsm"],
            "niskin bottle": table["niskin"],
            "temperature": table["t090c"],
            "salinity": table["sal00"],
            "oxygen": table["sbox0mm_kg"],
            "chlorophyll": table["chlorophyll"],
        }
    )


def main() -> None:
    OUTFILE.parent.mkdir(exist_ok=True)
    data = pd.concat([cruise_table(cruise) for cruise in CRUISES], ignore_index=True)
    data.sort_values(["timestamp", "cast", "niskin bottle"]).to_csv(
        OUTFILE, index=False
    )
    print(f"Wrote {len(data)} rows to {OUTFILE}")


if __name__ == "__main__":
    main()
