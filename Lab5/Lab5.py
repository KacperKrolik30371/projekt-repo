import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv("Online_Retail.csv", encoding="latin1")
df2 = pd.read_csv("Online_Retail_II.csv", encoding="latin1")

df = pd.concat([df1, df2], ignore_index=True)

df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month

print("=== OLAP: Roll-up (rok) ===")
rollup_year = df.groupby("Year")["TotalPrice"].sum()
print(rollup_year)

print("=== OLAP: Drill-down (rok, miesiąc) ===")
drilldown = df.groupby(["Year", "Month"])["TotalPrice"].sum()
print(drilldown)

print("=== OLAP: Slice (UK) ===")
slice_uk = df[df["Country"] == "United Kingdom"]
slice_uk_result = slice_uk.groupby("Year")["TotalPrice"].sum()
print(slice_uk_result)

print("=== OLAP: Dice (UK, 2011) ===")
dice = df[(df["Country"] == "United Kingdom") & (df["Year"] == 2011)]
dice_result = dice.groupby("Month")["TotalPrice"].sum()
print(dice_result)

print("=== OLAP: Pivot ===")
pivot = pd.pivot_table(
    df,
    values="TotalPrice",
    index="Country",
    columns="Year",
    aggfunc="sum"
)
print(pivot)

print("=== Zadanie 1: Top 10 krajów ===")
top10_countries = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top10_countries)

print("=== Zadanie 2: Sprzedaż miesięczna ===")
monthly_sales = (
    df.groupby("Month")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
)
print(monthly_sales)

print("=== Zadanie 2: Najlepszy miesiąc ===")
best_month = monthly_sales.idxmax()
best_value = monthly_sales.max()
print(best_month)
print(best_value)

print("=== Zadanie 3: Kostka (kraj x miesiąc) ===")
cube = pd.pivot_table(
    df,
    values="TotalPrice",
    index="Country",
    columns="Month",
    aggfunc="sum"
)
print(cube)

print("=== Zadanie 4: Najlepszy rok dla każdego kraju ===")
country_year = df.groupby(["Country", "Year"])["TotalPrice"].sum().reset_index()
best_year_per_country = country_year.loc[
    country_year.groupby("Country")["TotalPrice"].idxmax()
]
print(best_year_per_country)

print("=== Zadanie 5: Top 5 produktów w każdym kraju ===")
top_products = (
    df.groupby(["Country", "StockCode"])["TotalPrice"]
    .sum()
    .reset_index()
)
top5_per_country = top_products.sort_values(
    ["Country", "TotalPrice"], ascending=[True, False]
).groupby("Country").head(5)
print(top5_per_country)

print("=== Bonus: Wizualizacja ===")
top10_countries.plot(kind="bar")
plt.title("Top 10 krajów")
plt.show()

print("=== Bonus: Heatmap (pivot) ===")
plt.imshow(cube.fillna(0))
plt.colorbar()
plt.title("Heatmap sprzedaży (kraj x miesiąc)")
plt.xlabel("Miesiąc")
plt.ylabel("Kraj")
plt.show()