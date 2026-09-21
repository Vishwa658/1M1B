import os
import pandas as pd

DATA_DIR = "data"


def load_groundwater_data():
    all_data = []

    for filename in os.listdir(DATA_DIR):

        if not filename.startswith("chennai_groundwater_"):
            continue

        if not filename.endswith(".csv"):
            continue

        path = os.path.join(DATA_DIR, filename)

        df = pd.read_csv(path)

        # Remove extra spaces from column names
        df.columns = df.columns.astype(str).str.strip()

        year = filename.replace(
            "chennai_groundwater_", ""
        ).replace(".csv", "")

        df["year"] = int(year)

        all_data.append(df)

    if not all_data:
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)


def clean_number(value):

    try:
        value = str(value).strip()

        if value in ["", "-", "NA", "N/A", "nan"]:
            return None

        return float(value)

    except (ValueError, TypeError):
        return None


def find_location(df, location):

    location = location.lower().strip()

    matches = df[
        df["Location"]
        .astype(str)
        .str.lower()
        .str.contains(location, na=False)
    ]

    return matches


def get_groundwater(location):

    df = load_groundwater_data()

    if df.empty:

        return {
            "status": "no_data",
            "message": "Groundwater dataset is not available."
        }

    matches = find_location(df, location)

    if matches.empty:

        return {
            "status": "no_data",
            "message": f"No groundwater record was found for '{location}'."
        }

    readings = []

    # Detect available month columns automatically
    month_columns = [
        column
        for column in [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]
        if column in matches.columns
    ]

    for year in sorted(matches["year"].unique()):

        year_rows = matches[
            matches["year"] == year
        ]

        for _, year_row in year_rows.iterrows():

            for month in month_columns:

                value = clean_number(
                    year_row[month]
                )

                if value is not None:

                    readings.append({
                        "year": int(year),
                        "month": month,
                        "depth_m": value
                    })

    if not readings:

        return {
            "status": "no_data",
            "message": "The location exists in the dataset, but no usable groundwater reading was found."
        }

    # Sort readings chronologically
    month_order = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    readings.sort(
        key=lambda item: (
            item["year"],
            month_order[item["month"]]
        )
    )

    latest = readings[-1]

    previous = (
        readings[-2]
        if len(readings) > 1
        else None
    )

    change = None

    if previous:

        change = round(
            latest["depth_m"] - previous["depth_m"],
            2
        )

    first_row = matches.iloc[0]

    return {

        "status": "available",

        "location": location,

        "area_no": str(
            first_row.get("Area No.", "")
        ),

        "department_no": str(
            first_row.get("Dept No.", "")
        ),

        "latest": latest,

        "previous": previous,

        "change_m": change,

        "readings": readings,

        "source":
            "CMWSSB ward-wise groundwater monitoring data published through OpenCity",

        "data_type":
            "Historical/archived monitoring data",

        "warning":
            "This is depth-to-groundwater data measured below ground level. "
            "A larger depth generally means the water table is deeper. "
            "This value alone should not be treated as an official "
            "safe/danger classification."
    }