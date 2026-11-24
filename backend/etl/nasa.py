import pandas as pd
NASA_CSV_PATH = "data/raw/GLB.Ts+dSST.csv"

SOURCE = {
    "name": "NASA GISS Surface Temperature Analysis (GISTEMP v4)",
    "url": "https://data.giss.nasa.gov/gistemp/",
    "license": "Public domain (NASA)",
}

INDICATORS = [
    {
        "code": "temperature_anomaly",
        "name": "Global surface temperature anomaly",
        "unit": "°C",
        "frequency": "annual",
        "description": "Annual (Jan-Dec) global mean land-ocean surface temperature anomaly, relative to the 1951-1980 average.",
    },
]

def extract(data_source_url):
    nasa_df = pd.read_csv(data_source_url, skiprows=1, na_values="***")
    return nasa_df

def transform(df):
    nasa_df = df.copy()

    nasa_df = nasa_df[["Year", "J-D"]]
    nasa_df["country_code"] = "OWID_WRL"
    nasa_df["indicator_code"] = "temperature_anomaly"

    nasa_df = nasa_df.rename(columns={"J-D" : "value", "Year": "period"})

    nasa_df["period"] = pd.to_datetime(nasa_df["period"].astype(str) + "-01-01").dt.date

    nasa_df = nasa_df[["country_code", "period", "indicator_code", "value"]]
    nasa_df = nasa_df.dropna()

    nasa_country_df = pd.DataFrame([{"code": "OWID_WRL", "name": "World", "kind": "world"}])

    return nasa_country_df, nasa_df
