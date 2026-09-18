import pandas as pd
import re
import sqlite3

df = pd.read_csv("raw_scraped_listings.csv")
#price extraction, removal of commas, and conversion to float
df["Price_USD"] = df["raw_price"].str.extract(r"(\d[\d,.]+)")[0]
df["Price_USD"] = df["Price_USD"].str.replace(",","").astype(float)
#extract number of beds and bathrooms
df["Beds"] = df["raw_details"].str.extract(r"(\d+)\s*bed", flags=re.IGNORECASE)[0]
df["Baths"] = df["raw_details"].str.extract(r"(\d+)\s*bath", flags=re.IGNORECASE)[0]
#default bed and bath is set to 1
df["Beds"] = pd.to_numeric(df["Beds"].fillna(1).astype(int))
df["Baths"] = pd.to_numeric(df["Baths"].fillna(1).astype(int))
#extract state and city from location if available
df["City"] = df["raw_location"].apply(lambda x: str(x).split(",")[-2].strip() if pd.notnull(x) and "," in str(x) else "Unknown")
df["State"] = df["raw_location"].apply(lambda x: str(x).split(",")[-1].strip() if pd.notnull(x) and "," in str(x) else "Unknown")
#categorize listing based on price
df["Listing_Category"] = df["Price_USD"].apply(lambda x: "High End" if x>= 500000 else "Standard")
#drop rows without price
df_clean = df.dropna(subset=["Price_USD"]).copy()

df_clean.to_csv("data/clean_real_estate_pipeline.csv", index=False)

conn = sqlite3.connect("real_estate_market.db")
df_clean.to_sql("properties",conn, if_exists="replace",index=False)
conn.close()
print("Pipeline done successfully")
