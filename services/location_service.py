import pandas as pd


LOCATION_FILE = "data/chennai_locations.csv"


def load_locations():

    return pd.read_csv(
        LOCATION_FILE
    )


def find_location(location):

    df = load_locations()

    location = location.lower().strip()

    for _, row in df.iterrows():

        name = str(
            row["locality"]
        ).lower()

        aliases = str(
            row["aliases"]
        ).lower().split("|")

        if (
            location == name
            or location in aliases
        ):

            return {

                "locality": row["locality"],

                "zone": row["zone"],

                "ward": row["ward"]
            }

    return None