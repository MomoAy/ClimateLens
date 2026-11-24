import pandas as pd
OWID_CSV_PATH = "data/raw/owid-co2-data.csv"

SOURCE = {
    "name": "Our World in Data - CO2 and Greenhouse Gas Emissions",
    "url": "https://github.com/owid/co2-data",
    "license": "CC BY 4.0",
}

INDICATORS = [
    {
        "code": "co2",
        "name": "Annual CO2 emissions",
        "unit": "million tonnes (Mt)",
        "frequency": "annual",
        "description": "Annual total emissions of carbon dioxide (CO2), excluding land-use change. Source: Global Carbon Budget.",
    },
    {
        "code": "co2_per_capita",
        "name": "CO2 emissions per capita",
        "unit": "tonnes per person (t/person)",
        "frequency": "annual",
        "description": "Annual CO2 emissions from fossil fuels and industry, excluding land-use change, divided by population. Source: Global Carbon Budget.",
    },
]

def extract(data_source_url):
    owid_df = pd.read_csv(data_source_url)
    return owid_df

def transform(df):
    owid_df = df.copy()

    owid_df.loc[owid_df["country"] == "World", "iso_code"] = "OWID_WRL"
    owid_df = owid_df[owid_df["iso_code"].notna() & (owid_df["iso_code"].str.strip() != "")]
    
    owid_country_df = owid_df[["iso_code", "country"]].copy()
    owid_country_df["kind"] = "country"
    owid_country_df["continent"] = None
    owid_country_df = owid_country_df.rename(columns={"iso_code": "code", "country": "name"})
    owid_country_df.loc[owid_country_df["code"] == "OWID_WRL", "kind"] = "world"

    owid_df = owid_df[["iso_code", "year", "co2", "co2_per_capita"]]
    owid_df_melted = owid_df.melt(
        id_vars=["iso_code", "year"],
        var_name="variable",
        value_name="value"
    )
    owid_df_melted = owid_df_melted.rename(columns={"iso_code": "country_code", "variable" : "indicator_code", "year": "period"})
    owid_df_melted["period"] = pd.to_datetime(owid_df_melted["period"].astype(str) + "-01-01").dt.date
    owid_df_melted = owid_df_melted.dropna()
    owid_country_df = owid_country_df.drop_duplicates()

    return owid_country_df, owid_df_melted

