import pandas as pd
from pathlib import Path

# --- Paths ---
BASE_PATH = Path(__file__).resolve().parents[2]

BRONZE = BASE_PATH / "data" / "bronze"
GOLD = BASE_PATH / "data" / "gold"

GLOBAL_WEEKLY_FILE = BRONZE / "global_weekly.xlsx"
COUNTRY_WEEKLY_FILE = BRONZE / "country_weekly.xlsx"
GLOBAL_ALLTIME_FILE = BRONZE / "global_alltime.xlsx"

OUTPUT_FILE = GOLD / "netflix_final.parquet"


# --- Load ---
def load_data():
    df_global_weekly = pd.read_excel(GLOBAL_WEEKLY_FILE)
    df_country_weekly = pd.read_excel(COUNTRY_WEEKLY_FILE)
    df_global_alltime = pd.read_excel(GLOBAL_ALLTIME_FILE)

    return df_global_weekly, df_country_weekly, df_global_alltime


# --- Clean ---
def clean_data(df):
    # lowercase all column names
    df.columns = df.columns.str.lower()

    # standardize join column
    if "show_title" in df.columns:
        df["show_title"] = df["show_title"].str.strip().str.lower()

    return df


# --- Transform ---
def transform_data(df_global_weekly, df_country_weekly, df_global_alltime):

    # Clean all datasets
    df_global_weekly = clean_data(df_global_weekly)
    df_country_weekly = clean_data(df_country_weekly)
    df_global_alltime = clean_data(df_global_alltime)

    # UNION weekly datasets
    df_weekly = pd.concat(
        [df_global_weekly, df_country_weekly],
        ignore_index=True
    )

    # JOIN with all-time dataset
    df_final = df_weekly.merge(
        df_global_alltime,
        on="show_title",
        how="left"
    )

    return df_final


# --- Save ---
def save_data(df):
    GOLD.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        OUTPUT_FILE,
        engine="pyarrow",
        index=False
    )

    print(f"[SUCCESS] Saved dataset → {OUTPUT_FILE}")


# --- Main ---
def main():
    df_global_weekly, df_country_weekly, df_global_alltime = load_data()

    df_final = transform_data(
        df_global_weekly,
        df_country_weekly,
        df_global_alltime
    )

    save_data(df_final)


if __name__ == "__main__":
    main()