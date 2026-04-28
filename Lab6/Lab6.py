import pandas as pd

df1 = pd.read_csv("Online_Retail.csv", encoding="latin1")
df2 = pd.read_csv("Online_Retail_II.csv", encoding="latin1")

df = pd.concat([df1, df2], ignore_index=True)

df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month

print("=== Zadanie 1: Tabela pivot ===")
pivot = df.pivot_table(
    values="Revenue",
    index="Country",
    columns="Month",
    aggfunc="sum"
)
print(pivot)

monthly_totals = pivot.sum(axis=0)
best_month = monthly_totals.idxmax()
print("Najlepszy miesiąc:", best_month)

print("=== Zadanie 2: Ranking krajów ===")
ranking = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
top10 = ranking.head(10)
print(top10)

print("=== Zadanie 3: Analiza klientów ===")
customers = df.groupby("CustomerID")["Revenue"].sum()
top_customers = customers.sort_values(ascending=False).head(10)
avg_revenue = customers.mean()

print("Top 10 klientów")
print(top_customers)

print("Średni przychód na klienta")
print(avg_revenue)

print("=== Zadanie 4: Segmentacja krajów ===")
country_revenue = ranking

q1 = country_revenue.quantile(0.25)
q3 = country_revenue.quantile(0.75)

def segment(x):
    if x >= q3:
        return "Top 25%"
    elif x <= q1:
        return "Bottom 25%"
    else:
        return "Middle 50%"

segments = country_revenue.apply(segment)
segmented = pd.DataFrame({
    "Revenue": country_revenue,
    "Segment": segments
})

print(segmented)

print("=== Zadanie 5: Wnioski ===")
print("Kluczowe kraje:")
print(top10.index.tolist())

print("Czy sprzedaż jest równomierna między krajami:")
print("Nie, większość przychodu generuje kilka krajów")

print("Czy widać sezonowość:")
print("Tak, niektóre miesiące mają wyraźnie wyższą sprzedaż")