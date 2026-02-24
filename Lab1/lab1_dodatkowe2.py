import pandas as pd

df = pd.read_csv("sales_raw.csv")

df = df.drop_duplicates()

df["total_price"] = df["quantity"] * df["unit_price"]

country_map = {
    "Poland": "PL",
    "Germany": "DE"
}

df["country"] = df["country"].map(country_map)

df["order_date"] = pd.to_datetime(df["order_date"])

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"] = df["order_date"].dt.day

q1 = df["unit_price"].quantile(0.25)
q3 = df["unit_price"].quantile(0.75)
iqr = q3 - q1

outliers = df[(df["unit_price"] < q1 - 1.5 * iqr) | (df["unit_price"] > q3 + 1.5 * iqr)]

print(df.head())
print(outliers)